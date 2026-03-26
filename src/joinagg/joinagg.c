#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *id;
    char *region;
    char *tier;
} User;

typedef struct {
    char *id;
    long long latency_ms;
    long long bytes;
} Event;

typedef struct {
    const char *region;
    const char *tier;
    long long latency_ms;
    long long bytes;
} Joined;

static void ensure_capacity(void **items, size_t *capacity, size_t len, size_t item_size) {
    if (len < *capacity) {
        return;
    }
    *capacity = *capacity ? *capacity * 2 : 1024;
    *items = realloc(*items, *capacity * item_size);
    if (*items == NULL) {
        perror("realloc");
        exit(1);
    }
}

static int cmp_users(const void *lhs, const void *rhs) {
    const User *a = (const User *)lhs;
    const User *b = (const User *)rhs;
    return strcmp(a->id, b->id);
}

static int cmp_events(const void *lhs, const void *rhs) {
    const Event *a = (const Event *)lhs;
    const Event *b = (const Event *)rhs;
    return strcmp(a->id, b->id);
}

static int cmp_joined(const void *lhs, const void *rhs) {
    const Joined *a = (const Joined *)lhs;
    const Joined *b = (const Joined *)rhs;
    int region_cmp = strcmp(a->region, b->region);
    if (region_cmp != 0) {
        return region_cmp;
    }
    return strcmp(a->tier, b->tier);
}

static char *dup_range(const char *start, size_t len) {
    char *out = malloc(len + 1);
    if (out == NULL) {
        perror("malloc");
        exit(1);
    }
    memcpy(out, start, len);
    out[len] = '\0';
    return out;
}

static void append_user(User **users, size_t *len, size_t *capacity, const char *line) {
    const char *first = strchr(line, ',');
    const char *second = first ? strchr(first + 1, ',') : NULL;
    const char *third = second ? strchr(second + 1, ',') : NULL;
    if (first == NULL || second == NULL || third == NULL) {
        return;
    }
    if (strcmp(third + 1, "active") != 0) {
        return;
    }
    ensure_capacity((void **)users, capacity, *len, sizeof(**users));
    (*users)[*len].id = dup_range(line, (size_t)(first - line));
    (*users)[*len].region = dup_range(first + 1, (size_t)(second - first - 1));
    (*users)[*len].tier = dup_range(second + 1, (size_t)(third - second - 1));
    *len += 1;
}

static void append_event(Event **events, size_t *len, size_t *capacity, const char *line) {
    const char *first = strchr(line, ',');
    const char *second = first ? strchr(first + 1, ',') : NULL;
    const char *third = second ? strchr(second + 1, ',') : NULL;
    if (first == NULL || second == NULL || third == NULL) {
        return;
    }
    if ((size_t)(second - first - 1) == 4 && memcmp(first + 1, "noop", 4) == 0) {
        return;
    }
    ensure_capacity((void **)events, capacity, *len, sizeof(**events));
    (*events)[*len].id = dup_range(line, (size_t)(first - line));
    (*events)[*len].latency_ms = strtoll(second + 1, NULL, 10);
    (*events)[*len].bytes = strtoll(third + 1, NULL, 10);
    *len += 1;
}

int main(void) {
    User *users = NULL;
    Event *events = NULL;
    Joined *joined = NULL;
    size_t users_len = 0;
    size_t users_capacity = 0;
    size_t events_len = 0;
    size_t events_capacity = 0;
    size_t joined_len = 0;
    size_t joined_capacity = 0;
    char *line = NULL;
    size_t line_capacity = 0;
    enum { SECTION_NONE, SECTION_USERS, SECTION_EVENTS } section = SECTION_NONE;
    int header_pending = 0;

    while (getline(&line, &line_capacity, stdin) >= 0) {
        size_t line_len = strcspn(line, "\r\n");
        line[line_len] = '\0';
        if (line[0] == '\0') {
            continue;
        }
        if (strcmp(line, "[users]") == 0) {
            section = SECTION_USERS;
            header_pending = 1;
            continue;
        }
        if (strcmp(line, "[events]") == 0) {
            section = SECTION_EVENTS;
            header_pending = 1;
            continue;
        }
        if (header_pending) {
            header_pending = 0;
            continue;
        }
        if (section == SECTION_USERS) {
            append_user(&users, &users_len, &users_capacity, line);
        } else if (section == SECTION_EVENTS) {
            append_event(&events, &events_len, &events_capacity, line);
        }
    }
    free(line);

    qsort(users, users_len, sizeof(*users), cmp_users);
    qsort(events, events_len, sizeof(*events), cmp_events);

    size_t i = 0;
    size_t j = 0;
    while (i < users_len && j < events_len) {
        int cmp = strcmp(users[i].id, events[j].id);
        if (cmp < 0) {
            i += 1;
        } else if (cmp > 0) {
            j += 1;
        } else {
            const User *current = &users[i];
            while (j < events_len && strcmp(current->id, events[j].id) == 0) {
                ensure_capacity((void **)&joined, &joined_capacity, joined_len, sizeof(*joined));
                joined[joined_len].region = current->region;
                joined[joined_len].tier = current->tier;
                joined[joined_len].latency_ms = events[j].latency_ms;
                joined[joined_len].bytes = events[j].bytes;
                joined_len += 1;
                j += 1;
            }
            i += 1;
        }
    }

    qsort(joined, joined_len, sizeof(*joined), cmp_joined);

    i = 0;
    while (i < joined_len) {
        const char *region = joined[i].region;
        const char *tier = joined[i].tier;
        long long count = 0;
        long long latency_sum = 0;
        long long bytes_sum = 0;
        while (i < joined_len && strcmp(region, joined[i].region) == 0 && strcmp(tier, joined[i].tier) == 0) {
            count += 1;
            latency_sum += joined[i].latency_ms;
            bytes_sum += joined[i].bytes;
            i += 1;
        }
        printf("%s,%s,%lld,%lld,%lld\n", region, tier, count, latency_sum, bytes_sum);
    }

    for (i = 0; i < users_len; i++) {
        free(users[i].id);
        free(users[i].region);
        free(users[i].tier);
    }
    for (i = 0; i < events_len; i++) {
        free(events[i].id);
    }
    free(users);
    free(events);
    free(joined);
    return 0;
}
