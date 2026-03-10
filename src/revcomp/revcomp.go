package main

import (
	"bufio"
	"bytes"
	"os"
)

const revWidth = 60

var complementTable [256]byte

func init() {
	for i := 0; i < len(complementTable); i++ {
		complementTable[i] = byte(i)
	}
	from := []byte("ACBDGHKMNSRUTWVYacbdghkmnsrutwvy")
	to := []byte("TGVHCDMKNSYAAWBRTgvhcdmknsyaawbr")
	for i, ch := range from {
		complementTable[ch] = to[i]
	}
}

func emitRecord(w *bufio.Writer, header []byte, sequence []byte) {
	if len(header) == 0 {
		return
	}
	w.Write(header)
	w.WriteByte('\n')
	line := make([]byte, 0, revWidth)
	for i := len(sequence) - 1; i >= 0; i-- {
		line = append(line, complementTable[sequence[i]])
		if len(line) == revWidth {
			w.Write(line)
			w.WriteByte('\n')
			line = line[:0]
		}
	}
	if len(line) > 0 {
		w.Write(line)
		w.WriteByte('\n')
	}
}

func main() {
	input, _ := os.ReadFile("/dev/stdin")
	lines := bytes.Split(input, []byte{'\n'})
	header := make([]byte, 0, 128)
	sequence := make([]byte, 0, len(input))
	writer := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer writer.Flush()

	for _, raw := range lines {
		line := bytes.TrimSuffix(raw, []byte{'\r'})
		if len(line) > 0 && line[0] == '>' {
			emitRecord(writer, header, sequence)
			header = append(header[:0], line...)
			sequence = sequence[:0]
			continue
		}
		for _, ch := range line {
			if ch != '\r' && ch != ' ' && ch != '\t' {
				sequence = append(sequence, ch)
			}
		}
	}
	emitRecord(writer, header, sequence)
}
