package main

import (
	"fmt"
	"os"
	"strconv"
)

func reversePrefix(values []int, count int) {
	i := 0
	j := count - 1
	for i < j {
		values[i], values[j] = values[j], values[i]
		i++
		j--
	}
}

func fannkuch(n int) (int, int) {
	p := make([]int, n)
	q := make([]int, n)
	s := make([]int, n)
	for i := range p {
		p[i] = i
	}

	sign := 1
	maxFlips := 0
	sum := 0

	for {
		q0 := p[0]
		if q0 != 0 {
			copy(q[1:], p[1:])
			flips := 1
			for {
				reversePrefix(q[1:], q0-1)
				q[q0], q0 = q0, q[q0]
				if q0 == 0 {
					break
				}
				flips++
			}
			if flips > maxFlips {
				maxFlips = flips
			}
			sum += sign * flips
		}

		if sign == 1 {
			p[0], p[1] = p[1], p[0]
			sign = -1
			continue
		}

		p[1], p[2] = p[2], p[1]
		sign = 1
		done := true
		for i := 2; i < n; i++ {
			if s[i] < i {
				s[i]++
				done = false
				break
			}
			s[i] = 0
			first := p[0]
			copy(p[:i], p[1:i+1])
			p[i] = first
			if i == n-1 {
				return sum, maxFlips
			}
		}
		if !done {
			continue
		}
	}
}

func main() {
	n := 11
	if len(os.Args) > 1 {
		if value, err := strconv.Atoi(os.Args[1]); err == nil {
			n = value
		}
	}

	sum, maxFlips := fannkuch(n)
	fmt.Printf("%d\nPfannkuchen(%d) = %d\n", sum, n, maxFlips)
}
