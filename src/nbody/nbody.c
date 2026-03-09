#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  double x;
  double y;
  double z;
  double vx;
  double vy;
  double vz;
  double mass;
} Body;

static const double SOLAR_MASS = 4.0 * M_PI * M_PI;
static const double DAYS_PER_YEAR = 365.24;

static Body make_body(
    double x,
    double y,
    double z,
    double vx,
    double vy,
    double vz,
    double mass) {
  Body body = {
      .x = x,
      .y = y,
      .z = z,
      .vx = vx * DAYS_PER_YEAR,
      .vy = vy * DAYS_PER_YEAR,
      .vz = vz * DAYS_PER_YEAR,
      .mass = mass * SOLAR_MASS,
  };
  return body;
}

static void advance(Body *bodies, int count, double dt) {
  for (int i = 0; i < count; ++i) {
    for (int j = i + 1; j < count; ++j) {
      double dx = bodies[i].x - bodies[j].x;
      double dy = bodies[i].y - bodies[j].y;
      double dz = bodies[i].z - bodies[j].z;
      double distance_sq = dx * dx + dy * dy + dz * dz;
      double distance = sqrt(distance_sq);
      double mag = dt / (distance_sq * distance);

      double m1 = bodies[i].mass;
      double m2 = bodies[j].mass;

      bodies[i].vx -= dx * m2 * mag;
      bodies[i].vy -= dy * m2 * mag;
      bodies[i].vz -= dz * m2 * mag;
      bodies[j].vx += dx * m1 * mag;
      bodies[j].vy += dy * m1 * mag;
      bodies[j].vz += dz * m1 * mag;
    }
  }

  for (int i = 0; i < count; ++i) {
    bodies[i].x += dt * bodies[i].vx;
    bodies[i].y += dt * bodies[i].vy;
    bodies[i].z += dt * bodies[i].vz;
  }
}

static double energy(const Body *bodies, int count) {
  double result = 0.0;
  for (int i = 0; i < count; ++i) {
    result += 0.5 * bodies[i].mass *
              (bodies[i].vx * bodies[i].vx + bodies[i].vy * bodies[i].vy +
               bodies[i].vz * bodies[i].vz);
    for (int j = i + 1; j < count; ++j) {
      double dx = bodies[i].x - bodies[j].x;
      double dy = bodies[i].y - bodies[j].y;
      double dz = bodies[i].z - bodies[j].z;
      double distance = sqrt(dx * dx + dy * dy + dz * dz);
      result -= (bodies[i].mass * bodies[j].mass) / distance;
    }
  }
  return result;
}

static void offset_momentum(Body *bodies, int count) {
  double px = 0.0;
  double py = 0.0;
  double pz = 0.0;
  for (int i = 0; i < count; ++i) {
    px += bodies[i].vx * bodies[i].mass;
    py += bodies[i].vy * bodies[i].mass;
    pz += bodies[i].vz * bodies[i].mass;
  }
  bodies[0].vx = -px / SOLAR_MASS;
  bodies[0].vy = -py / SOLAR_MASS;
  bodies[0].vz = -pz / SOLAR_MASS;
}

int main(int argc, char **argv) {
  long iterations = argc > 1 ? strtol(argv[1], NULL, 10) : 10000000L;
  Body bodies[] = {
      {.x = 0.0, .y = 0.0, .z = 0.0, .vx = 0.0, .vy = 0.0, .vz = 0.0, .mass = SOLAR_MASS},
      make_body(4.84143144246472090e+00, -1.16032004402742839e+00,
                -1.03622044471123109e-01, 1.66007664274403694e-03,
                7.69901118419740425e-03, -6.90460016972063023e-05,
                9.54791938424326609e-04),
      make_body(8.34336671824457987e+00, 4.12479856412430479e+00,
                -4.03523417114321381e-01, -2.76742510726862411e-03,
                4.99852801234917238e-03, 2.30417297573763929e-05,
                2.85885980666130812e-04),
      make_body(1.28943695621391310e+01, -1.51111514016986312e+01,
                -2.23307578892655734e-01, 2.96460137564761618e-03,
                2.37847173959480950e-03, -2.96589568540237556e-05,
                4.36624404335156298e-05),
      make_body(1.53796971148509165e+01, -2.59193146099879641e+01,
                1.79258772950371181e-01, 2.68067772490389322e-03,
                1.62824170038242295e-03, -9.51592254519715870e-05,
                5.15138902046611451e-05),
  };
  const int count = (int)(sizeof(bodies) / sizeof(bodies[0]));

  offset_momentum(bodies, count);
  printf("%.9f\n", energy(bodies, count));
  for (long i = 0; i < iterations; ++i) {
    advance(bodies, count, 0.01);
  }
  printf("%.9f\n", energy(bodies, count));
  return 0;
}
