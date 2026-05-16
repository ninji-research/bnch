#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static bool is_prime(int n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (int i = 3; n / i >= i; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 50000;
    int count = 0;
    for (int i = 2; i <= n; i++) {
        if (is_prime(i)) count++;
    }
    printf("%d\n", count);
    return 0;
}
