#include <stdio.h>
#include <pigpio.h> 
#include <string.h>
// Konfigurasi pin sesuai wiring
#define EN_A 5     // PIN 7
#define IN1 17     // PIN 11
#define IN2 27     // PIN 13
int main() {
    // Inisialisasi library pigpio
    if (gpioInitialise() < 0) {
        fprintf(stderr, "Gagal inisialisasi GPIO\n");
        return 1;
    }
    // Setup mode pin
    gpioSetMode(EN_A, PI_OUTPUT);  // PWM
    gpioSetMode(IN1, PI_OUTPUT);   // Control
    gpioSetMode(IN2, PI_OUTPUT);   // Control
    // Set arah putaran motor (IN1 HIGH, IN2 LOW)
    gpioWrite(IN1, 1);
    gpioWrite(IN2, 0);
    int pwm = 0;
    printf("Kontrol PWM Pompa (0-255). Ketik 'exit' untuk keluar\n");
    while(1) {
        printf("Masukkan nilai PWM: ");
        char input[10];
        fgets(input, sizeof(input), stdin);

        // Exit condition
        if(strcmp(input, "exit\n") == 0) break;

        // Konversi input ke integer
        if(sscanf(input, "%d", &pwm) != 1) {
            printf("Input tidak valid!\n");
            continue;
        }
        // Clamp nilai PWM 0-255
        pwm = (pwm < 0) ? 0 : (pwm > 255) ? 255 : pwm;

        // Terapkan PWM ke motor
        gpioPWM(EN_A, pwm);
        printf("PWM diatur ke: %d\n\n", pwm);
    }
    // Cleanup
    gpioPWM(EN_A, 0);     // Matikan motor
    gpioWrite(IN1, 0);     // Reset pin kontrol
    gpioWrite(IN2, 0);
    gpioTerminate();
    return 0;
}
