#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int size = argc > 1 ? atoi(argv[1]) : 4000;
    uint32_t sum = 0;

    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size / 8; ++x) {
            int byte = 0;
            for (int b = 0; b < 8; ++b) {
                double ci = ((double)y * 2.0) / (double)size - 1.0;
                double cr = ((double)(x * 8 + b) * 2.0) / (double)size - 1.5;
                double zr = 0.0;
                double zi = 0.0;
                double tr = 0.0;
                double ti = 0.0;
                int i = 0;
                while (i < 50 && tr + ti <= 4.0) {
                    zi = 2.0 * zr * zi + ci;
                    zr = tr - ti + cr;
                    tr = zr * zr;
                    ti = zi * zi;
                    ++i;
                }
                if (tr + ti <= 4.0) {
                    byte |= 1 << (7 - b);
                }
            }
            sum += (uint32_t)byte;
        }
    }

    printf("%u\n", sum);
    return 0;
}
