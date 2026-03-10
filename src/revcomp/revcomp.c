#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WIDTH 60

typedef struct {
    char *data;
    size_t len;
    size_t cap;
} Buffer;

static unsigned char complement_table[256];

static void buffer_push(Buffer *buffer, char ch) {
    if (buffer->len == buffer->cap) {
        buffer->cap = buffer->cap ? buffer->cap * 2 : 1024;
        buffer->data = realloc(buffer->data, buffer->cap);
        if (!buffer->data) {
            fputs("allocation failure\n", stderr);
            exit(1);
        }
    }
    buffer->data[buffer->len++] = ch;
}

static void init_complements(void) {
    for (int i = 0; i < 256; i++) {
        complement_table[i] = (unsigned char)i;
    }
    const char *from = "ACBDGHKMNSRUTWVYacbdghkmnsrutwvy";
    const char *to = "TGVHCDMKNSYAAWBRTgvhcdmknsyaawbr";
    for (size_t i = 0; from[i] != '\0'; i++) {
        complement_table[(unsigned char)from[i]] = (unsigned char)to[i];
    }
}

static void emit_sequence(const Buffer *sequence) {
    if (sequence->len == 0) {
        return;
    }
    char line[WIDTH];
    size_t line_len = 0;
    for (size_t i = sequence->len; i-- > 0;) {
        line[line_len++] = (char)complement_table[(unsigned char)sequence->data[i]];
        if (line_len == WIDTH) {
            fwrite(line, 1, WIDTH, stdout);
            putchar('\n');
            line_len = 0;
        }
    }
    if (line_len > 0) {
        fwrite(line, 1, line_len, stdout);
        putchar('\n');
    }
}

static void flush_record(const Buffer *header, const Buffer *sequence) {
    if (header->len == 0) {
        return;
    }
    fwrite(header->data, 1, header->len, stdout);
    putchar('\n');
    emit_sequence(sequence);
}

int main(void) {
    init_complements();

    Buffer header = {0};
    Buffer sequence = {0};
    char *line = NULL;
    size_t cap = 0;
    ssize_t len;

    while ((len = getline(&line, &cap, stdin)) != -1) {
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) {
            len--;
        }
        if (len > 0 && line[0] == '>') {
            flush_record(&header, &sequence);
            header.len = 0;
            sequence.len = 0;
            for (ssize_t i = 0; i < len; i++) {
                buffer_push(&header, line[i]);
            }
            continue;
        }
        for (ssize_t i = 0; i < len; i++) {
            unsigned char ch = (unsigned char)line[i];
            if (!isspace(ch)) {
                buffer_push(&sequence, (char)ch);
            }
        }
    }

    flush_record(&header, &sequence);
    free(line);
    free(header.data);
    free(sequence.data);
    return 0;
}
