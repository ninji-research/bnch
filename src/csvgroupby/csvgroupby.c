#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *customer;
    long long qty;
    long long cents;
} Row;

static int cmp_rows(const void *lhs, const void *rhs) {
    const Row *a = (const Row *)lhs;
    const Row *b = (const Row *)rhs;
    return strcmp(a->customer, b->customer);
}

static void ensure_capacity(Row **rows, size_t *capacity, size_t len) {
    if (len < *capacity) {
        return;
    }
    *capacity = *capacity ? *capacity * 2 : 1024;
    *rows = realloc(*rows, *capacity * sizeof(**rows));
    if (*rows == NULL) {
        perror("realloc");
        exit(1);
    }
}

int main(void) {
    Row *rows = NULL;
    size_t len = 0;
    size_t capacity = 0;
    char *line = NULL;
    size_t line_capacity = 0;

    if (getline(&line, &line_capacity, stdin) < 0) {
        free(line);
        return 0;
    }

    while (getline(&line, &line_capacity, stdin) >= 0) {
        char *first = strchr(line, ',');
        char *second = first ? strchr(first + 1, ',') : NULL;
        char *third = second ? strchr(second + 1, ',') : NULL;
        if (first == NULL || second == NULL || third == NULL) {
            continue;
        }
        *first = '\0';
        *second = '\0';
        *third = '\0';

        ensure_capacity(&rows, &capacity, len);
        rows[len].customer = strdup(line);
        rows[len].qty = strtoll(second + 1, NULL, 10);
        rows[len].cents = strtoll(third + 1, NULL, 10);
        if (rows[len].customer == NULL) {
            perror("strdup");
            exit(1);
        }
        len += 1;
    }
    free(line);

    qsort(rows, len, sizeof(*rows), cmp_rows);

    size_t i = 0;
    while (i < len) {
        const char *customer = rows[i].customer;
        long long count = 0;
        long long qty_sum = 0;
        long long cents_sum = 0;
        do {
            count += 1;
            qty_sum += rows[i].qty;
            cents_sum += rows[i].cents;
            i += 1;
        } while (i < len && strcmp(customer, rows[i].customer) == 0);
        printf("%s,%lld,%lld,%lld\n", customer, count, qty_sum, cents_sum);
    }

    for (i = 0; i < len; i++) {
        free(rows[i].customer);
    }
    free(rows);
    return 0;
}
