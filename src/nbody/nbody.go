package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

const (
	solarMass   = 4.0 * math.Pi * math.Pi
	daysPerYear = 365.24
)

type body struct {
	x, y, z    float64
	vx, vy, vz float64
	mass       float64
}

func newBody(x, y, z, vx, vy, vz, mass float64) body {
	return body{
		x:    x,
		y:    y,
		z:    z,
		vx:   vx * daysPerYear,
		vy:   vy * daysPerYear,
		vz:   vz * daysPerYear,
		mass: mass * solarMass,
	}
}

func advance(bodies []body, dt float64) {
	for i := 0; i < len(bodies); i++ {
		for j := i + 1; j < len(bodies); j++ {
			dx := bodies[i].x - bodies[j].x
			dy := bodies[i].y - bodies[j].y
			dz := bodies[i].z - bodies[j].z
			distanceSq := dx*dx + dy*dy + dz*dz
			distance := math.Sqrt(distanceSq)
			mag := dt / (distanceSq * distance)

			m1 := bodies[i].mass
			m2 := bodies[j].mass

			bodies[i].vx -= dx * m2 * mag
			bodies[i].vy -= dy * m2 * mag
			bodies[i].vz -= dz * m2 * mag
			bodies[j].vx += dx * m1 * mag
			bodies[j].vy += dy * m1 * mag
			bodies[j].vz += dz * m1 * mag
		}
	}

	for i := range bodies {
		bodies[i].x += dt * bodies[i].vx
		bodies[i].y += dt * bodies[i].vy
		bodies[i].z += dt * bodies[i].vz
	}
}

func energy(bodies []body) float64 {
	result := 0.0
	for i := 0; i < len(bodies); i++ {
		result += 0.5 * bodies[i].mass * (bodies[i].vx*bodies[i].vx + bodies[i].vy*bodies[i].vy + bodies[i].vz*bodies[i].vz)
		for j := i + 1; j < len(bodies); j++ {
			dx := bodies[i].x - bodies[j].x
			dy := bodies[i].y - bodies[j].y
			dz := bodies[i].z - bodies[j].z
			distance := math.Sqrt(dx*dx + dy*dy + dz*dz)
			result -= (bodies[i].mass * bodies[j].mass) / distance
		}
	}
	return result
}

func offsetMomentum(bodies []body) {
	px := 0.0
	py := 0.0
	pz := 0.0
	for i := range bodies {
		px += bodies[i].vx * bodies[i].mass
		py += bodies[i].vy * bodies[i].mass
		pz += bodies[i].vz * bodies[i].mass
	}
	bodies[0].vx = -px / solarMass
	bodies[0].vy = -py / solarMass
	bodies[0].vz = -pz / solarMass
}

func main() {
	iterations := int64(10000000)
	if len(os.Args) > 1 {
		if value, err := strconv.ParseInt(os.Args[1], 10, 64); err == nil {
			iterations = value
		}
	}

	bodies := []body{
		{x: 0.0, y: 0.0, z: 0.0, vx: 0.0, vy: 0.0, vz: 0.0, mass: solarMass},
		newBody(4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01, 1.66007664274403694e-03, 7.69901118419740425e-03, -6.90460016972063023e-05, 9.54791938424326609e-04),
		newBody(8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01, -2.76742510726862411e-03, 4.99852801234917238e-03, 2.30417297573763929e-05, 2.85885980666130812e-04),
		newBody(1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01, 2.96460137564761618e-03, 2.37847173959480950e-03, -2.96589568540237556e-05, 4.36624404335156298e-05),
		newBody(1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01, 2.68067772490389322e-03, 1.62824170038242295e-03, -9.51592254519715870e-05, 5.15138902046611451e-05),
	}

	offsetMomentum(bodies)
	fmt.Printf("%.9f\n", energy(bodies))
	for i := int64(0); i < iterations; i++ {
		advance(bodies, 0.01)
	}
	fmt.Printf("%.9f\n", energy(bodies))
}
