#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double eval_a(int i, int j) {
  int ij = i + j;
  return 1.0 / (double)((ij * (ij + 1) / 2) + i + 1);
}

static void eval_a_times_u(const double *u, double *au, int n) {
  for (int i = 0; i < n; ++i) {
    double sum = 0.0;
    for (int j = 0; j < n; ++j) {
      sum += eval_a(i, j) * u[j];
    }
    au[i] = sum;
  }
}

static void eval_at_times_u(const double *u, double *au, int n) {
  for (int i = 0; i < n; ++i) {
    double sum = 0.0;
    for (int j = 0; j < n; ++j) {
      sum += eval_a(j, i) * u[j];
    }
    au[i] = sum;
  }
}

static void eval_ata_times_u(const double *u, double *v, double *w, int n) {
  eval_a_times_u(u, w, n);
  eval_at_times_u(w, v, n);
}

int main(int argc, char **argv) {
  int n = argc > 1 ? atoi(argv[1]) : 5500;
  double *u = malloc((size_t)n * sizeof(*u));
  double *v = malloc((size_t)n * sizeof(*v));
  double *w = malloc((size_t)n * sizeof(*w));
  if (u == NULL || v == NULL || w == NULL) {
    free(u);
    free(v);
    free(w);
    return 1;
  }

  for (int i = 0; i < n; ++i) {
    u[i] = 1.0;
    v[i] = 0.0;
    w[i] = 0.0;
  }

  for (int i = 0; i < 10; ++i) {
    eval_ata_times_u(u, v, w, n);
    eval_ata_times_u(v, u, w, n);
  }

  double vbv = 0.0;
  double vv = 0.0;
  for (int i = 0; i < n; ++i) {
    vbv += u[i] * v[i];
    vv += v[i] * v[i];
  }

  printf("%.9f\n", sqrt(vbv / vv));
  free(u);
  free(v);
  free(w);
  return 0;
}
