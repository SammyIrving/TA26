/*
 * KONTROL DEBIT POMPA – TRIMMED-MEAN + KALIBRASI POLINOMIAL DERAJAT 2 + LOOPING OTOMATIS
 */

#include "sensirion_common.h"
#include "sensirion_i2c_hal.h"
#include "sf06_lf_i2c.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pigpio.h>
#include <math.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <sys/select.h>

#define EN_A                  5       // GPIO pin untuk kontrol PWM pompa

// Flow Parameters (ml/min)
#define MIN_FLOW              31
#define MID_FLOW              46
#define MAX_FLOW              61

// PWM Parameters (0–255)
#define MIN_PWM               76
#define MID_PWM               100
#define MAX_PWM               130

// Timing & Sampling
#define STABILIZE_DELAY_US    400000UL   // 0.4 s tunggu flow stabil
#define SAMPLE_PERIOD_US      20000UL    // 0.02 s antar sampel
#define N_SAMPLES             600
#define TRIM_PERCENT          5

#define SENSOR_I2C_ADDR       SLF3S_4000B_I2C_ADDR_08
#define SENSOR_SCALE_FACTOR   INV_FLOW_SCALE_FACTORS_SLF3S_4000B
#define sensirion_hal_sleep_us sensirion_i2c_hal_sleep_usec

// Polynomial calibration coefficients (degree 2)
static const float CAL_A2 = 0.0132468245f;
static const float CAL_A1 = -0.4932028720f;
static const float CAL_A0 = 37.7446506000f;

// Calibration using polynomial
static float apply_poly_calibration(float raw) {
    return CAL_A2 * raw * raw + CAL_A1 * raw + CAL_A0;
}

// Compare floats for qsort
static int cmpf(const void *a, const void *b) {
    float fa = *(const float*)a, fb = *(const float*)b;
    return (fa < fb) ? -1 : (fa > fb) ? 1 : 0;
}

// Map target flow to PWM value
static int mapFlowToPWM(int flow) {
    if (flow <= MID_FLOW) {
        return (int)((flow - MIN_FLOW) / (float)(MID_FLOW - MIN_FLOW)
                     * (MID_PWM - MIN_PWM) + MIN_PWM);
    } else {
        return (int)((flow - MID_FLOW) / (float)(MAX_FLOW - MID_FLOW)
                     * (MAX_PWM - MID_PWM) + MID_PWM);
    }
}

// Check for non-blocking key press
static int kbhit(void) {
    struct timeval tv = { 0L, 0L };
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(STDIN_FILENO, &fds);
    return select(STDIN_FILENO+1, &fds, NULL, NULL, &tv);
}

int main(void) {
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    // canonical mode + echo
    newt.c_lflag |= ICANON;
    newt.c_lflag |= ECHO;
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    if (gpioInitialise() < 0) {
        fprintf(stderr, "GPIO initialization failed\n");
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        return 1;
    }
    gpioSetMode(EN_A, PI_OUTPUT);

    printf("=== SISTEM KONTROL DEBIT POMPA – POLINOMIAL KALIBRASI DERAJAT 2 ===\n"
           "Range debit: %d–%d ml/min\nKetik 'x' atau 'exit' pada input target untuk keluar\n\n",
           MIN_FLOW, MAX_FLOW);

    char input[32];
    sensirion_i2c_hal_init();
    sf06_lf_init(SENSOR_I2C_ADDR);

    while (1) {
        printf("Masukkan debit yang diinginkan (ml/min): ");
        fflush(stdout);
        if (!fgets(input, sizeof(input), stdin)) break;
        input[strcspn(input, "\n")] = '\0';
        if (strcmp(input, "exit") == 0 || strcmp(input, "x") == 0) {
            gpioPWM(EN_A, 0);
            printf("Pompa dihentikan dan program keluar!\n");
            break;
        }

        char *endptr;
        long target_flow = strtol(input, &endptr, 10);
        if (*endptr != '\0' || target_flow < MIN_FLOW || target_flow > MAX_FLOW) {
            printf("Input tidak valid! Masukkan nilai antara %d–%d\n\n", MIN_FLOW, MAX_FLOW);
            continue;
        }

        int pwm = mapFlowToPWM((int)target_flow);
        gpioPWM(EN_A, pwm);
        printf("\n> PWM diset ke %d untuk target %ld ml/min\n", pwm, target_flow);
        printf("  Menunggu stabilisasi (%.2f s)...\n", STABILIZE_DELAY_US/1e6);
        sensirion_hal_sleep_us(STABILIZE_DELAY_US);

        sf06_lf_stop_continuous_measurement();
        sensirion_hal_sleep_us(100000);
        sf06_lf_start_h2o_continuous_measurement();
        sensirion_hal_sleep_us(50000);

        printf("Pengukuran kontinu dimulai. Ketik 'x' lalu Enter untuk berhenti pengukuran.\n\n");

        while (1) {
            float samples[N_SAMPLES];
            int cnt = 0;

            for (int i = 0; i < N_SAMPLES; ++i) {
                sensirion_hal_sleep_us(SAMPLE_PERIOD_US);
                float raw, temp;
                uint16_t flags;
                if (sf06_lf_read_measurement_data(
                        SENSOR_SCALE_FACTOR, &raw, &temp, &flags) == NO_ERROR) {
                    samples[cnt++] = raw;
                }
                if (i % 50 == 0 && kbhit()) {
                    fgets(input, sizeof(input), stdin);
                    input[strcspn(input, "\n")] = '\0';
                    if (strcmp(input, "x") == 0 || strcmp(input, "exit") == 0) {
                        printf("Pengukuran dihentikan oleh user.\n\n");
                        gpioPWM(EN_A, 0);
                        sf06_lf_stop_continuous_measurement();
                        goto end_measurement;
                    }
                }
            }

            if (cnt == 0) {
                printf("Gagal mendapatkan data sensor!\n\n");
                break;
            }

            qsort(samples, cnt, sizeof(float), cmpf);
            int trim = cnt * TRIM_PERCENT / 100;
            float sum = 0;
            for (int i = trim; i < cnt - trim; ++i) {
                sum += samples[i];
            }
            float trimmed_mean = sum / (cnt - 2 * trim);
            float calibrated_flow = apply_poly_calibration(trimmed_mean);

            printf("Flow terkalibrasi: %.2f ml/min\n", calibrated_flow);
        }
    end_measurement:
        ;
    }

    gpioPWM(EN_A, 0);
    gpioTerminate();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt); // Restore terminal mode
    return 0;
}
