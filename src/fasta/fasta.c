#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WIDTH 60
#define IM 139968
#define IA 3877
#define IC 29573

typedef struct {
    char ch;
    double p;
} AminoAcid;

static const char ALU[] =
    "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG"
    "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA"
    "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT"
    "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA"
    "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG"
    "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC"
    "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA";

static const AminoAcid IUB[] = {
    {'a', 0.27}, {'c', 0.12}, {'g', 0.12}, {'t', 0.27}, {'B', 0.02}, {'D', 0.02},
    {'H', 0.02}, {'K', 0.02}, {'M', 0.02}, {'N', 0.02}, {'R', 0.02}, {'S', 0.02},
    {'V', 0.02}, {'W', 0.02}, {'Y', 0.02},
};

static const AminoAcid HOMO_SAPIENS[] = {
    {'a', 0.3029549426680},
    {'c', 0.1979883004921},
    {'g', 0.1975473066391},
    {'t', 0.3015094502008},
};

static uint32_t seed = 42;

static double next_random(void) {
    seed = (seed * IA + IC) % IM;
    return (double)seed / (double)IM;
}

static void write_repeat(const char *header, const char *sequence, int length) {
    const int seq_len = (int)strlen(sequence);
    int offset = 0;
    puts(header);
    while (length > 0) {
        const int line_len = length < WIDTH ? length : WIDTH;
        for (int i = 0; i < line_len; i++) {
            putchar(sequence[(offset + i) % seq_len]);
        }
        putchar('\n');
        offset = (offset + line_len) % seq_len;
        length -= line_len;
    }
}

static void build_cumulative(const AminoAcid *source, int count, AminoAcid *dest) {
    double total = 0.0;
    for (int i = 0; i < count; i++) {
        total += source[i].p;
        dest[i].ch = source[i].ch;
        dest[i].p = total;
    }
}

static char select_random(const AminoAcid *table, int count) {
    const double value = next_random();
    for (int i = 0; i < count; i++) {
        if (value < table[i].p) {
            return table[i].ch;
        }
    }
    return table[count - 1].ch;
}

static void write_random(const char *header, const AminoAcid *table, int count, int length) {
    char line[WIDTH];
    puts(header);
    while (length > 0) {
        const int line_len = length < WIDTH ? length : WIDTH;
        for (int i = 0; i < line_len; i++) {
            line[i] = select_random(table, count);
        }
        fwrite(line, 1, (size_t)line_len, stdout);
        putchar('\n');
        length -= line_len;
    }
}

int main(int argc, char **argv) {
    const int n = argc > 1 ? atoi(argv[1]) : 250000;
    AminoAcid iub[sizeof(IUB) / sizeof(IUB[0])];
    AminoAcid homo[sizeof(HOMO_SAPIENS) / sizeof(HOMO_SAPIENS[0])];

    build_cumulative(IUB, (int)(sizeof(IUB) / sizeof(IUB[0])), iub);
    build_cumulative(HOMO_SAPIENS, (int)(sizeof(HOMO_SAPIENS) / sizeof(HOMO_SAPIENS[0])), homo);

    write_repeat(">ONE Homo sapiens alu", ALU, n * 2);
    write_random(">TWO IUB ambiguity codes", iub, (int)(sizeof(iub) / sizeof(iub[0])), n * 3);
    write_random(">THREE Homo sapiens frequency", homo, (int)(sizeof(homo) / sizeof(homo[0])), n * 5);
    return 0;
}
