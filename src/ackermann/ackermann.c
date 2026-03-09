#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static uint32_t ackermann(uint32_t m, uint32_t n) {
    if (m == 0) {
        return n + 1;
    }
    if (n == 0) {
        return ackermann(m - 1, 1);
    }
    return ackermann(m - 1, ackermann(m, n - 1));
}

int main(int argc, char **argv) {
    uint32_t m = argc > 1 ? (uint32_t)strtoul(argv[1], NULL, 10) : 3U;
    uint32_t n = argc > 2 ? (uint32_t)strtoul(argv[2], NULL, 10) : 11U;
    printf("%u\n", ackermann(m, n));
    return 0;
}
