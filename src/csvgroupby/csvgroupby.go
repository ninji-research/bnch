package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type stats struct {
	count int64
	qty   int64
	cents int64
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1024), 1024*1024)
	if !scanner.Scan() {
		return
	}

	aggregates := make(map[string]stats)
	for scanner.Scan() {
		line := scanner.Text()
		first := strings.IndexByte(line, ',')
		second := strings.IndexByte(line[first+1:], ',')
		third := strings.IndexByte(line[first+1+second+1:], ',')
		customer := line[:first]
		qty, _ := strconv.ParseInt(line[first+1+second+1:first+1+second+1+third], 10, 64)
		cents, _ := strconv.ParseInt(line[first+1+second+1+third+1:], 10, 64)

		value := aggregates[customer]
		value.count++
		value.qty += qty
		value.cents += cents
		aggregates[customer] = value
	}

	keys := make([]string, 0, len(aggregates))
	for key := range aggregates {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	writer := bufio.NewWriterSize(os.Stdout, 1<<20)
	for _, key := range keys {
		value := aggregates[key]
		fmt.Fprintf(writer, "%s,%d,%d,%d\n", key, value.count, value.qty, value.cents)
	}
	writer.Flush()
}
