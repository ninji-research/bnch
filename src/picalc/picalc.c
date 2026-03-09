#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  uint32_t seed;
  long iterations;
  long inside;
} WorkerArgs;

static double xorshift32(uint32_t *state) {
  uint32_t x = *state;
  x ^= x << 13;
  x ^= x >> 17;
  x ^= x << 5;
  *state = x;
  return (double)x / 4294967295.0;
}

static void *worker(void *arg) {
  WorkerArgs *job = (WorkerArgs *)arg;
  uint32_t state = job->seed;
  long inside = 0;

  for (long i = 0; i < job->iterations; ++i) {
    double x = xorshift32(&state);
    double y = xorshift32(&state);
    if (x * x + y * y <= 1.0) {
      ++inside;
    }
  }

  job->inside = inside;
  return NULL;
}

int main(int argc, char **argv) {
  long total_iterations = argc > 1 ? strtol(argv[1], NULL, 10) : 50000000L;
  int threads = argc > 2 ? atoi(argv[2]) : 4;
  if (threads < 1) {
    threads = 1;
  }

  pthread_t *handles = malloc((size_t)threads * sizeof(*handles));
  WorkerArgs *jobs = malloc((size_t)threads * sizeof(*jobs));
  if (handles == NULL || jobs == NULL) {
    free(handles);
    free(jobs);
    return 1;
  }

  for (int i = 0; i < threads; ++i) {
    long start = (total_iterations * i) / threads;
    long end = (total_iterations * (i + 1)) / threads;
    jobs[i].seed = 12345u + (uint32_t)i;
    jobs[i].iterations = end - start;
    jobs[i].inside = 0;
    if (pthread_create(&handles[i], NULL, worker, &jobs[i]) != 0) {
      free(handles);
      free(jobs);
      return 1;
    }
  }

  long total_inside = 0;
  for (int i = 0; i < threads; ++i) {
    pthread_join(handles[i], NULL);
    total_inside += jobs[i].inside;
  }

  printf("%.5f\n", 4.0 * (double)total_inside / (double)total_iterations);
  free(handles);
  free(jobs);
  return 0;
}
