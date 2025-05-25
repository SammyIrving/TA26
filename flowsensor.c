#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pigpio.h>
#include "sensirion_common.h"
#include "sensirion_i2c_hal.h"
#include "sf06_lf_i2c.h"
#include <curl/curl.h>

// GPIO Configuration
#define EN_A 5       // GPIO 4 (PWM) - Only using this pin for pump control

// Flow Parameters
#define MIN_FLOW 31
#define MID_FLOW 46
#define MAX_FLOW 61

// PWM Parameters
#define MIN_PWM 73
#define MID_PWM 94
#define MAX_PWM 125

// Sensor Parameters
#define SENSOR_ADDR SLF3S_4000B_I2C_ADDR_08
#define DELAY_FLOW_SENSOR 400000  // 400ms

// Measurement Parameters
#define SCALE_FACTOR 37
#define N_AVERAGE 20
// N Repetition = 150/minute x time (minute)
#define N_REPETITION 2250  // For 15 minutes measurement

// Function to map flow rate to PWM value
int mapFlowToPWM(int flow) {
    if(flow <= MID_FLOW) {
        return (int)((float)(flow - MIN_FLOW)/(MID_FLOW - MIN_FLOW)*(MID_PWM - MIN_PWM) + MIN_PWM);
    } else {
        return (int)((float)(flow - MID_FLOW)/(MAX_FLOW - MID_FLOW)*(MAX_PWM - MID_PWM) + MID_PWM);
    }
}

void print_byte_array(uint8_t* array, uint16_t len) {
    uint16_t i = 0;
    printf("0x");
    for (; i < len; i++) {
        printf("%02x", array[i]);
    }
}

void send_to_python(float value) {
    CURL *curl;
    CURLcode res;
    char postfields[100];

    snprintf(postfields, sizeof(postfields), "{\"value\": %.2f}", value);

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5000/receive_data");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postfields);

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        } else {
            printf("Data sent: %.2f\n", value);
        }

        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }

    curl_global_cleanup();
}


int main() {
    // Initialize GPIO
    if(gpioInitialise() < 0) {
        fprintf(stderr, "GPIO initialization failed\n");
        return 1;
    }

    // Setup GPIO pin
    gpioSetMode(EN_A, PI_OUTPUT);

    printf("Pump Control and Flow Measurement System\n");
    printf("Input flow rate (%d-%d ml/min)\n", MIN_FLOW, MAX_FLOW);
    printf("Ketik 'x' atau 'exit' untuk keluar\n");

    char input[20];
    
    while(1) {
        printf("\nMasukkan debit (ml/min): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0;  // Remove newline

        if(strcmp(input, "exit") == 0 || strcmp(input, "x") == 0) {
            gpioPWM(EN_A, 0);  // Stop the pump
            printf("Pompa dihentikan!\n");
            break;
        }

        // Process flow input
        char *endptr;
        long flow = strtol(input, &endptr, 10);
        
        if(*endptr == '\0' && flow >= MIN_FLOW && flow <= MAX_FLOW) {
            int target_flow = (int)flow;
            int pwm = mapFlowToPWM(target_flow);
            gpioPWM(EN_A, pwm);
            
            printf("Debit diatur ke %d ml/min (PWM: %d)\n", target_flow, pwm);
            printf("Memulai pengukuran...\n");
            
            // Initialize Flow Sensor
            int16_t error = NO_ERROR;
            sensirion_i2c_hal_init();
            sf06_lf_init(SENSOR_ADDR);

            sf06_lf_stop_continuous_measurement();
            sensirion_i2c_hal_sleep_usec(100000);
            
            uint32_t product_identifier = 0;
            uint8_t serial_number[8] = {0};
            error = sf06_lf_read_product_identifier(&product_identifier, serial_number, 8);
            
            if (error != NO_ERROR) {
                printf("Error executing read_product_identifier(): %i\n", error);
                continue;
            }
            
            printf("Product Identifier: %u\n", product_identifier);
            printf("Serial Number: ");
            print_byte_array(serial_number, 8);
            printf("\n");
            
            error = sf06_lf_start_h2o_continuous_measurement();
            if (error != NO_ERROR) {
                printf("Error executing start_h2o_continuous_measurement(): %i\n", error);
                continue;
            }
            
            float a_flow = 0.0;
            float a_temperature = 0.0;
            uint16_t a_signaling_flags = 0u;
            uint16_t repetition = 0;
            float a_flow_20 = 0.0;
            int flag_tampil_flow = 0;    
            float total = 0.0;
            
            printf("Pengukuran dimulai. Target flow rate: %d ml/min (PWM: %d)\n", target_flow, pwm);
            
            for (repetition = 0; repetition < N_REPETITION; repetition++) {
                flag_tampil_flow++;
                sensirion_i2c_hal_sleep_usec(DELAY_FLOW_SENSOR);
                
                error = sf06_lf_read_measurement_data(SCALE_FACTOR, &a_flow, &a_temperature, &a_signaling_flags);
                if (error != NO_ERROR) {
                    printf("Error executing read_measurement_data(): %i\n", error);
                    continue;
                }

                a_flow_20 += a_flow;
                total += a_flow;

                if (flag_tampil_flow > N_AVERAGE) {
                    printf("Measured Flow (ml/min) = %.2f\n", a_flow_20/(N_AVERAGE+1));
                    float test_value = a_flow_20/(N_AVERAGE+1);
                    send_to_python(test_value);
                    flag_tampil_flow = 0;
                    a_flow_20 = 0.0;
                }
                
                // Check if user wants to stop measurement early
                struct timeval tv = {0, 0};
                fd_set fds;
                FD_ZERO(&fds);
                FD_SET(0, &fds);
                
                if(select(1, &fds, NULL, NULL, &tv) > 0) {
                    char stop_input[10];
                    fgets(stop_input, sizeof(stop_input), stdin);
                    if (stop_input[0] == 'x' || stop_input[0] == 'q') {
                        printf("Pengukuran dihentikan oleh pengguna.\n");
                        break;
                    }
                }
            }
            
            // Calculate average flow
            float avg_flow = total / repetition;
            printf("\n--- PENGUKURAN SELESAI ---\n");
            printf("Total pengukuran: %d sampel\n", repetition);
            printf("Flow rate rata-rata: %.2f ml/min\n", avg_flow);
            
            error = sf06_lf_stop_continuous_measurement();
            if (error != NO_ERROR) {
                printf("Error stopping measurement: %i\n", error);
            }
            
        } else {
            printf("Input tidak valid! Masukkan nilai antara %d-%d atau 'x'\n", MIN_FLOW, MAX_FLOW);
        }
    }

    // Cleanup
    gpioTerminate();
    return 0;
}
