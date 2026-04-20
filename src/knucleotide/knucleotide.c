#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char key[3];
    int count;
} Entry;

static const char *TARGETS[] = {
    "GGT",
    "GGTA",
    "GGTATT",
    "GGTATTTTAATT",
    "GGTATTTTAATTTATAGT",
};

static void fail(void) {
    fputs("allocation failure\n", stderr);
    exit(1);
}

static int encode_base(char ch) {
    switch (ch) {
        case 'A': return 0;
        case 'C': return 1;
        case 'G': return 2;
        case 'T': return 3;
        default: return -1;
    }
}

static char decode_base(int code) {
    static const char ALPHABET[] = {'A', 'C', 'G', 'T'};
    return ALPHABET[code & 3];
}

static char *read_three_sequence(size_t *out_len) {
    char *line = NULL;
    size_t line_cap = 0;
    ssize_t line_len;
    int in_three = 0;

    char *seq = NULL;
    size_t len = 0;
    size_t cap = 0;

    while ((line_len = getline(&line, &line_cap, stdin)) != -1) {
        if (line[0] == '>') {
            if (in_three) {
                break;
            }
            in_three = strncmp(line, ">THREE", 6) == 0;
            continue;
        }
        if (!in_three) {
            continue;
        }
        for (ssize_t i = 0; i < line_len; ++i) {
            unsigned char ch = (unsigned char)line[i];
            if (!isalpha(ch)) {
                continue;
            }
            if (len == cap) {
                size_t next_cap = cap == 0 ? 4096 : cap * 2;
                char *next = realloc(seq, next_cap);
                if (next == NULL) {
                    fail();
                }
                seq = next;
                cap = next_cap;
            }
            seq[len++] = (char)toupper(ch);
        }
    }
    free(line);

    if (seq == NULL) {
        seq = malloc(1);
        if (seq == NULL) {
            fail();
        }
    }
    *out_len = len;
    return seq;
}

static int entry_cmp(const void *lhs, const void *rhs) {
    const Entry *a = lhs;
    const Entry *b = rhs;
    if (a->count != b->count) {
        return b->count - a->count;
    }
    return strcmp(a->key, b->key);
}

static void print_frequencies(const char *sequence, size_t seq_len, int k) {
    if (seq_len < (size_t)k) {
        putchar('\n');
        return;
    }

    const int bucket_count = 1 << (2 * k);
    const int mask = bucket_count - 1;
    int *counts = calloc((size_t)bucket_count, sizeof(*counts));
    if (counts == NULL) {
        fail();
    }

    int rolling = 0;
    for (int i = 0; i < k; ++i) {
        rolling = (rolling << 2) | encode_base(sequence[i]);
    }
    counts[rolling] += 1;
    for (size_t i = (size_t)k; i < seq_len; ++i) {
        rolling = ((rolling << 2) & mask) | encode_base(sequence[i]);
        counts[rolling] += 1;
    }

    Entry *entries = malloc((size_t)bucket_count * sizeof(*entries));
    if (entries == NULL) {
        free(counts);
        fail();
    }

    int len = 0;
    for (int code = 0; code < bucket_count; ++code) {
        if (counts[code] == 0) {
            continue;
        }
        for (int i = k - 1, value = code; i >= 0; --i, value >>= 2) {
            entries[len].key[i] = decode_base(value);
        }
        entries[len].key[k] = '\0';
        entries[len].count = counts[code];
        len += 1;
    }

    qsort(entries, (size_t)len, sizeof(*entries), entry_cmp);
    const double total = (double)(seq_len - (size_t)k + 1);
    for (int i = 0; i < len; ++i) {
        printf("%s %.3f\n", entries[i].key, 100.0 * (double)entries[i].count / total);
    }
    putchar('\n');

    free(entries);
    free(counts);
}

static int count_fragment(const char *sequence, size_t seq_len, const char *target) {
    const size_t target_len = strlen(target);
    if (seq_len < target_len) {
        return 0;
    }
    int count = 0;
    for (size_t i = 0; i + target_len <= seq_len; ++i) {
        if (memcmp(sequence + i, target, target_len) == 0) {
            count += 1;
        }
    }
    return count;
}

int main(void) {
    size_t seq_len = 0;
    char *sequence = read_three_sequence(&seq_len);

    print_frequencies(sequence, seq_len, 1);
    print_frequencies(sequence, seq_len, 2);
    for (size_t i = 0; i < sizeof(TARGETS) / sizeof(TARGETS[0]); ++i) {
        printf("%d\t%s\n", count_fragment(sequence, seq_len, TARGETS[i]), TARGETS[i]);
    }

    free(sequence);
    return 0;
}
