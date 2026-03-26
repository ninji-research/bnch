#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void ensure_capacity(char ***items, size_t *capacity, size_t len) {
    if (len < *capacity) {
        return;
    }
    *capacity = *capacity ? *capacity * 2 : 1024;
    *items = realloc(*items, *capacity * sizeof(**items));
    if (*items == NULL) {
        perror("realloc");
        exit(1);
    }
}

static int cmp_strings(const void *lhs, const void *rhs) {
    const char *const *a = (const char *const *)lhs;
    const char *const *b = (const char *const *)rhs;
    return strcmp(*a, *b);
}

int main(void) {
    char **words = NULL;
    size_t len = 0;
    size_t capacity = 0;
    char *line = NULL;
    size_t line_capacity = 0;

    while (getline(&line, &line_capacity, stdin) >= 0) {
        size_t line_len = strcspn(line, "\r\n");
        if (line_len == 0) {
            continue;
        }
        line[line_len] = '\0';
        ensure_capacity(&words, &capacity, len);
        words[len] = strdup(line);
        if (words[len] == NULL) {
            perror("strdup");
            exit(1);
        }
        len += 1;
    }
    free(line);

    qsort(words, len, sizeof(*words), cmp_strings);
    for (size_t i = 0; i < len;) {
        const char *word = words[i];
        size_t count = 0;
        do {
            count += 1;
            i += 1;
        } while (i < len && strcmp(word, words[i]) == 0);
        printf("%s,%zu\n", word, count);
    }

    for (size_t i = 0; i < len; i++) {
        free(words[i]);
    }
    free(words);
    return 0;
}
