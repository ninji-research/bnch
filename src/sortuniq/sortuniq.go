package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1024), 1024*1024)
	words := make([]string, 0, 1<<18)
	for scanner.Scan() {
		word := scanner.Text()
		if word != "" {
			words = append(words, word)
		}
	}

	sort.Strings(words)

	writer := bufio.NewWriterSize(os.Stdout, 1<<20)
	for i := 0; i < len(words); {
		word := words[i]
		count := 1
		i++
		for i < len(words) && words[i] == word {
			count++
			i++
		}
		fmt.Fprintf(writer, "%s,%d\n", word, count)
	}
	writer.Flush()
}
