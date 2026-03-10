package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const (
	width = 60
	im    = 139968
	ia    = 3877
	ic    = 29573
)

type aminoAcid struct {
	ch byte
	p  float64
}

var alu = "" +
	"GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" +
	"GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA" +
	"CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT" +
	"ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA" +
	"GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG" +
	"AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC" +
	"AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA"

var iub = []aminoAcid{
	{'a', 0.27}, {'c', 0.12}, {'g', 0.12}, {'t', 0.27}, {'B', 0.02}, {'D', 0.02},
	{'H', 0.02}, {'K', 0.02}, {'M', 0.02}, {'N', 0.02}, {'R', 0.02}, {'S', 0.02},
	{'V', 0.02}, {'W', 0.02}, {'Y', 0.02},
}

var homoSapiens = []aminoAcid{
	{'a', 0.3029549426680},
	{'c', 0.1979883004921},
	{'g', 0.1975473066391},
	{'t', 0.3015094502008},
}

var seed uint32 = 42

func nextRandom() float64 {
	seed = (seed*ia + ic) % im
	return float64(seed) / float64(im)
}

func buildCumulative(source []aminoAcid) []aminoAcid {
	result := make([]aminoAcid, len(source))
	total := 0.0
	for i, item := range source {
		total += item.p
		result[i] = aminoAcid{ch: item.ch, p: total}
	}
	return result
}

func writeRepeat(w *bufio.Writer, header string, sequence string, length int) {
	fmt.Fprintln(w, header)
	offset := 0
	for length > 0 {
		lineLen := width
		if length < lineLen {
			lineLen = length
		}
		line := make([]byte, lineLen)
		for i := 0; i < lineLen; i++ {
			line[i] = sequence[(offset+i)%len(sequence)]
		}
		w.Write(line)
		w.WriteByte('\n')
		offset = (offset + lineLen) % len(sequence)
		length -= lineLen
	}
}

func pick(table []aminoAcid) byte {
	value := nextRandom()
	for _, item := range table {
		if value < item.p {
			return item.ch
		}
	}
	return table[len(table)-1].ch
}

func writeRandom(w *bufio.Writer, header string, table []aminoAcid, length int) {
	fmt.Fprintln(w, header)
	line := make([]byte, width)
	for length > 0 {
		lineLen := width
		if length < lineLen {
			lineLen = length
		}
		for i := 0; i < lineLen; i++ {
			line[i] = pick(table)
		}
		w.Write(line[:lineLen])
		w.WriteByte('\n')
		length -= lineLen
	}
}

func main() {
	n := 250000
	if len(os.Args) > 1 {
		if parsed, err := strconv.Atoi(os.Args[1]); err == nil {
			n = parsed
		}
	}

	writer := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer writer.Flush()

	writeRepeat(writer, ">ONE Homo sapiens alu", alu, n*2)
	writeRandom(writer, ">TWO IUB ambiguity codes", buildCumulative(iub), n*3)
	writeRandom(writer, ">THREE Homo sapiens frequency", buildCumulative(homoSapiens), n*5)
}
