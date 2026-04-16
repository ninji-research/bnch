package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

func evalA(i, j int) float64 {
	ij := i + j
	return 1.0 / float64((ij*(ij+1)/2)+i+1)
}

func evalATimesU(u, au []float64, n int) {
	for i := 0; i < n; i++ {
		sum := 0.0
		for j := 0; j < n; j++ {
			sum += evalA(i, j) * u[j]
		}
		au[i] = sum
	}
}

func evalAtTimesU(u, au []float64, n int) {
	for i := 0; i < n; i++ {
		sum := 0.0
		for j := 0; j < n; j++ {
			sum += evalA(j, i) * u[j]
		}
		au[i] = sum
	}
}

func evalAtATimesU(u, v, w []float64, n int) {
	evalATimesU(u, w, n)
	evalAtTimesU(w, v, n)
}

func main() {
	n := 5500
	if len(os.Args) > 1 {
		if value, err := strconv.Atoi(os.Args[1]); err == nil {
			n = value
		}
	}

	u := make([]float64, n)
	v := make([]float64, n)
	w := make([]float64, n)
	for i := range u {
		u[i] = 1.0
	}

	for i := 0; i < 10; i++ {
		evalAtATimesU(u, v, w, n)
		evalAtATimesU(v, u, w, n)
	}

	vbv := 0.0
	vv := 0.0
	for i := 0; i < n; i++ {
		vbv += u[i] * v[i]
		vv += v[i] * v[i]
	}

	fmt.Printf("%.9f\n", math.Sqrt(vbv/vv))
}
