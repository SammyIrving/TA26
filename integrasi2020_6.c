#include "sensirion_common.h"
#include "sensirion_i2c_hal.h"
#include "sf06_lf_i2c.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pigpio.h>
#include <sys/select.h>
#include <unistd.h>
#include <math.h>

#define sensirion_hal_sleep_us sensirion_i2c_hal_sleep_usec
#define DELAY_FLOW_SENSOR 100000 // 100 ms delay between readings
#define N_REPETITION 2250        // Total number of measurements
#define SCALE_FACTOR 32
#define N_AVERAGE 50             // Number of readings for averaging
#define NO_FLOW_THRESHOLD 1    // For no flow

// GPIO Configuration
#define EN_A 5       // GPIO pin for pump PWM control
// Flow Parameters
#define MIN_FLOW 31  // ml/min
#define MAX_FLOW 61  // ml/min

// Lookup table for PWM to flow mapping
const float flows[] = {31.57, 35.08, 40.26, 45.45, 50.00, 55.04, 60.00, 61.22};
const int pwms[] = {74, 79, 86, 96, 105, 113, 124, 125};
const int TABLE_SIZE = 8;

// Lookup table for flow compensation
const float comp_flows[] = {31.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 61.0};
const float comp_corrections[] = {8.20, 7.88, 5.36, 0.34, 0.0, 2.8, 4.80, 6.80};
const int COMP_TABLE_SIZE = 8;

void print_byte_array(uint8_t* array, uint16_t len) {
    uint16_t i = 0;
    printf("0x");
    for (; i < len; i++) {
        printf("%02x", array[i]);
    }
}

float compensateFlow(float flow, float target_flow) {
    if (fabs(flow) < NO_FLOW_THRESHOLD) {
        return 0.0;
    }
    if (target_flow < MIN_FLOW) target_flow = MIN_FLOW;
    if (target_flow > MAX_FLOW) target_flow = MAX_FLOW;

    for (int i = 0; i < COMP_TABLE_SIZE; i++) {
        if (target_flow == comp_flows[i]) {
            return flow + comp_corrections[i];
        }
    }

    float offset = 0.0;
    int use_fixed_offset = 1;

    if (target_flow == 32.0) {
        offset = 5.0;
    } else if (target_flow >= 33.0 && target_flow <= 34.0) {
        offset = 6.0;
    } else if (target_flow >= 41.0 && target_flow <= 43.0) {
        offset = 3.0;
    } else if (target_flow >= 47.0 && target_flow <= 49.0) {
        offset = 0.0;
    } else if (target_flow >= 51.0 && target_flow <= 53.0) {
        offset = -3.50;
    } else if (target_flow == 54.0) {
        offset = -2.0;
    } else if (target_flow >= 56.0 && target_flow <= 57.0) {
        offset = -2.0;
    } else if (target_flow >= 58.0 && target_flow <= 59.0) {
        offset = 0.0;
    } else {
        use_fixed_offset = 0;
    }

    if (use_fixed_offset) {
        return flow + offset;
    }

    // If not in fixed offset range, use lookup table with linear interpolation
    for (int i = 0; i < COMP_TABLE_SIZE - 1; i++) {
        if (target_flow >= comp_flows[i] && target_flow <= comp_flows[i + 1]) {
            float fraction = (target_flow - comp_flows[i]) / (comp_flows[i + 1] - comp_flows[i]);
            float correction = comp_corrections[i] + fraction * (comp_corrections[i + 1] - comp_corrections[i]);
            return flow + correction;
        }
    }

    // Handle edge cases for lookup table
    if (target_flow <= comp_flows[0]) return flow + comp_corrections[0];
    return flow + comp_corrections[COMP_TABLE_SIZE - 1];
}

int mapFlowToPWM(float flow) {
    // Clamp flow to valid range
    if (flow < MIN_FLOW) flow = MIN_FLOW;
    if (flow > MAX_FLOW) flow = MAX_FLOW;

    // Find the appropriate interval in the lookup table
    for (int i = 0; i < TABLE_SIZE - 1; i++) {
        if (flow >= flows[i] && flow <= flows[i + 1]) {
            float fraction = (flow - flows[i]) / (flows[i + 1] - flows[i]);
            float pwm = pwms[i] + fraction * (pwms[i + 1] - pwms[i]);
            return (int)(pwm + 0.5);
        }
    }

    // Handle edge cases
    if (flow <= flows[0]) return pwms[0];
    return pwms[TABLE_SIZE - 1];
}

int main(void) {
    // Inisialisasi GPIO
    if (gpioInitialise() < 0) {
        fprintf(stderr, "Inisialisasi GPIO gagal\n");
        return 1;
    }
    gpioSetMode(EN_A, PI_OUTPUT);

    // Inisialisasi sensor flow
    int16_t error = NO_ERROR;
    sensirion_i2c_hal_init();
    sf06_lf_init(SLF3S_4000B_I2C_ADDR_08);
    sf06_lf_stop_continuous_measurement();
    sensirion_hal_sleep_us(100000);

    uint32_t product_identifier = 0;
    uint8_t serial_number[8] = {0};
    error = sf06_lf_read_product_identifier(&product_identifier, serial_number, 8);
    if (error != NO_ERROR) {
        printf("Gagal membaca product identifier: %i\n", error);
        return error;
    }

    error = sf06_lf_start_h2o_continuous_measurement();
    if (error != NO_ERROR) {
        printf("Gagal memulai pengukuran: %i\n", error);
        return error;
    }

    // Sensor warm-up
    float a_flow = 0.0, a_temp = 0.0;
    uint16_t a_flags = 0u;
    for (int i = 0; i < 20; i++) {
        sf06_lf_read_measurement_data(SCALE_FACTOR, &a_flow, &a_temp, &a_flags);
        sensirion_hal_sleep_us(DELAY_FLOW_SENSOR);
    }

    // Minta input pengguna untuk nilai flow
    char input[20];
    printf("Masukkan nilai flow yang diinginkan (ml/min) atau 'x' untuk keluar: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    if (strcmp(input, "x") == 0 || strcmp(input, "exit") == 0) {
        printf("Keluar dari program.\n");
        sf06_lf_stop_continuous_measurement();
        gpioPWM(EN_A, 0);
        gpioTerminate();
        return 0;
    }

    int flow;
    if (sscanf(input, "%d", &flow) != 1 || flow < MIN_FLOW || flow > MAX_FLOW) {
        printf("Input tidak valid atau di luar rentang (%d-%d ml/min)\n", MIN_FLOW, MAX_FLOW);
        sf06_lf_stop_continuous_measurement();
        gpioPWM(EN_A, 0);
        gpioTerminate();
        return 1;
    }

    int pwm = mapFlowToPWM(flow);
    gpioPWM(EN_A, pwm);
    printf("✓ Pompa dijalankan pada %d ml/min (PWM: %d)\n", flow, pwm);

    float flow_sum = 0.0;
    int reading_count = 0;
    int error_count = 0;
    char input_buf[20];
    int input_pos = 0;
    int stop_all = 0;

    while (reading_count < N_REPETITION && !stop_all) {
        fd_set readfds;
        FD_ZERO(&readfds);
        FD_SET(0, &readfds);
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = DELAY_FLOW_SENSOR;

        int ret = select(1, &readfds, NULL, NULL, &tv);

        if (ret > 0 && FD_ISSET(0, &readfds)) {
            char c;
            while (read(0, &c, 1) > 0) {
                if (c == '\n') {
                    input_buf[input_pos] = '\0';
                    if (strcmp(input_buf, "x") == 0 || strcmp(input_buf, "exit") == 0) {
                        printf("❌ Perintah keluar diterima. Menghentikan pompa...\n");
                        stop_all = 1;
                        break;
                    }
                    input_pos = 0;
                } else if (input_pos < sizeof(input_buf) - 1) {
                    input_buf[input_pos++] = c;
                }
            }
        } else if (ret == 0) {
            error = sf06_lf_read_measurement_data(SCALE_FACTOR, &a_flow, &a_temp, &a_flags);
            if (error != NO_ERROR) {
                error_count++;
                if (error_count >= 5) {
                    printf("❌ Terlalu banyak error pengukuran. Menghentikan...\n");
                    break;
                }
                continue;
            }

            error_count = 0;
            a_flow = compensateFlow(a_flow, flow);
            flow_sum += a_flow;
            reading_count++;

            if (reading_count % N_AVERAGE == 0) {
                float average_flow = flow_sum / N_AVERAGE;
                printf("Flow Terukur (ml/min) = %.2f\n", average_flow);
                flow_sum = 0.0;
            }
        }
    }

    gpioPWM(EN_A, 0);
    sf06_lf_stop_continuous_measurement();
    gpioTerminate();
    return 0;
}
