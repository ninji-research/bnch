package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

type entry struct {
	key   string
	count int
}

var targets = []string{
	"GGT",
	"GGTA",
	"GGTATT",
	"GGTATTTTAATT",
	"GGTATTTTAATTTATAGT",
}

func encodeBase(ch byte) int {
	switch ch {
	case 'A':
		return 0
	case 'C':
		return 1
	case 'G':
		return 2
	case 'T':
		return 3
	default:
		return -1
	}
}

func decodeBase(code int) byte {
	return "ACGT"[code&3]
}

func readThreeSequence() []byte {
	scanner := bufio.NewScanner(os.Stdin)
	var sequence []byte
	inThree := false
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, ">") {
			if inThree {
				break
			}
			inThree = strings.HasPrefix(line, ">THREE")
			continue
		}
		if !inThree {
			continue
		}
		for i := 0; i < len(line); i++ {
			ch := line[i]
			if 'a' <= ch && ch <= 'z' {
				ch -= 'a' - 'A'
			}
			if encodeBase(ch) >= 0 {
				sequence = append(sequence, ch)
			}
		}
	}
	return sequence
}

func printFrequencies(sequence []byte, k int) {
	if len(sequence) < k {
		fmt.Println()
		return
	}
	bucketCount := 1 << (2 * k)
	mask := bucketCount - 1
	counts := make([]int, bucketCount)
	rolling := 0
	for i := 0; i < k; i++ {
		rolling = (rolling << 2) | encodeBase(sequence[i])
	}
	counts[rolling]++
	for i := k; i < len(sequence); i++ {
		rolling = ((rolling << 2) & mask) | encodeBase(sequence[i])
		counts[rolling]++
	}

	entries := make([]entry, 0, bucketCount)
	for code, count := range counts {
		if count == 0 {
			continue
		}
		key := make([]byte, k)
		value := code
		for i := k - 1; i >= 0; i-- {
			key[i] = decodeBase(value)
			value >>= 2
		}
		entries = append(entries, entry{key: string(key), count: count})
	}
	sort.Slice(entries, func(i, j int) bool {
		if entries[i].count != entries[j].count {
			return entries[i].count > entries[j].count
		}
		return entries[i].key < entries[j].key
	})

	total := float64(len(sequence) - k + 1)
	for _, entry := range entries {
		fmt.Printf("%s %.3f\n", entry.key, 100.0*float64(entry.count)/total)
	}
	fmt.Println()
}

func countFragment(sequence []byte, target string) int {
	fragment := []byte(target)
	count := 0
	for i := 0; i+len(fragment) <= len(sequence); i++ {
		match := true
		for j := 0; j < len(fragment); j++ {
			if sequence[i+j] != fragment[j] {
				match = false
				break
			}
		}
		if match {
			count++
		}
	}
	return count
}

func main() {
	sequence := readThreeSequence()
	printFrequencies(sequence, 1)
	printFrequencies(sequence, 2)
	for _, target := range targets {
		fmt.Printf("%d\t%s\n", countFragment(sequence, target), target)
	}
}
