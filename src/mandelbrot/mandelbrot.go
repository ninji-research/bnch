package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	size := 4000
	if len(os.Args) > 1 {
		if value, err := strconv.Atoi(os.Args[1]); err == nil {
			size = value
		}
	}

	invSize := 2.0 / float64(size)
	var sum uint32

	for y := 0; y < size; y++ {
		ci := float64(y)*invSize - 1.0
		for x := 0; x < size/8; x++ {
			var b byte
			for bit := 0; bit < 8; bit++ {
				cr := float64(x*8+bit)*invSize - 1.5
				zr := 0.0
				zi := 0.0
				tr := 0.0
				ti := 0.0
				i := 0
				for i < 50 && tr+ti <= 4.0 {
					zi = 2.0*zr*zi + ci
					zr = tr - ti + cr
					tr = zr * zr
					ti = zi * zi
					i++
				}
				if tr+ti <= 4.0 {
					b |= 1 << (7 - bit)
				}
			}
			sum += uint32(b)
		}
	}

	fmt.Println(sum)
}
