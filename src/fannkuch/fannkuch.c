#include <stdio.h>
#include <stdlib.h>

static void reverse_prefix(int *values, int count) {
    int i = 0;
    int j = count - 1;
    while (i < j) {
        int temp = values[i];
        values[i] = values[j];
        values[j] = temp;
        ++i;
        --j;
    }
}

static void fannkuch(int n, int *sum_out, int *max_flips_out) {
    int *p = (int *)malloc((size_t)n * sizeof(int));
    int *q = (int *)malloc((size_t)n * sizeof(int));
    int *s = (int *)calloc((size_t)n, sizeof(int));
    if (p == NULL || q == NULL || s == NULL) {
        perror("malloc");
        exit(1);
    }

    for (int i = 0; i < n; ++i) {
        p[i] = i;
    }

    int sign = 1;
    int max_flips = 0;
    int sum = 0;

    for (;;) {
        int q0 = p[0];
        if (q0 != 0) {
            for (int i = 1; i < n; ++i) {
                q[i] = p[i];
            }

            int flips = 1;
            for (;;) {
                reverse_prefix(q + 1, q0 - 1);
                int temp = q[q0];
                q[q0] = q0;
                q0 = temp;
                if (q0 == 0) {
                    break;
                }
                ++flips;
            }

            if (flips > max_flips) {
                max_flips = flips;
            }
            sum += sign * flips;
        }

        if (sign == 1) {
            int temp = p[0];
            p[0] = p[1];
            p[1] = temp;
            sign = -1;
        } else {
            int temp = p[1];
            p[1] = p[2];
            p[2] = temp;
            sign = 1;

            for (int i = 2; i < n; ++i) {
                int sx = s[i];
                if (sx < i) {
                    s[i] = sx + 1;
                    goto next_permutation;
                }
                s[i] = 0;
                temp = p[0];
                for (int j = 0; j < i; ++j) {
                    p[j] = p[j + 1];
                }
                p[i] = temp;
                if (i == n - 1) {
                    free(p);
                    free(q);
                    free(s);
                    *sum_out = sum;
                    *max_flips_out = max_flips;
                    return;
                }
            }
        }

    next_permutation:
        ;
    }
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 11;
    int sum = 0;
    int max_flips = 0;
    fannkuch(n, &sum, &max_flips);
    printf("%d\nPfannkuchen(%d) = %d\n", sum, n, max_flips);
    return 0;
}
