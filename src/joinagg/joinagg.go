package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type user struct {
	id     string
	region string
	tier   string
}

type event struct {
	id        string
	latencyMS int64
	bytes     int64
}

type joined struct {
	region    string
	tier      string
	latencyMS int64
	bytes     int64
}

func parseUser(line string) (user, bool) {
	first := strings.IndexByte(line, ',')
	second := strings.IndexByte(line[first+1:], ',')
	third := strings.IndexByte(line[first+1+second+1:], ',')
	status := line[first+1+second+1+third+1:]
	if status != "active" {
		return user{}, false
	}
	return user{
		id:     line[:first],
		region: line[first+1 : first+1+second],
		tier:   line[first+1+second+1 : first+1+second+1+third],
	}, true
}

func parseEvent(line string) (event, bool) {
	first := strings.IndexByte(line, ',')
	second := strings.IndexByte(line[first+1:], ',')
	third := strings.IndexByte(line[first+1+second+1:], ',')
	kind := line[first+1 : first+1+second]
	if kind == "noop" {
		return event{}, false
	}
	latencyMS, _ := strconv.ParseInt(line[first+1+second+1:first+1+second+1+third], 10, 64)
	bytes, _ := strconv.ParseInt(line[first+1+second+1+third+1:], 10, 64)
	return event{id: line[:first], latencyMS: latencyMS, bytes: bytes}, true
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1024), 4*1024*1024)
	users := make([]user, 0, 1<<15)
	events := make([]event, 0, 1<<18)
	section := ""
	headerPending := false

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}
		if line == "[users]" || line == "[events]" {
			section = line
			headerPending = true
			continue
		}
		if headerPending {
			headerPending = false
			continue
		}
		if section == "[users]" {
			if row, ok := parseUser(line); ok {
				users = append(users, row)
			}
		} else if section == "[events]" {
			if row, ok := parseEvent(line); ok {
				events = append(events, row)
			}
		}
	}

	sort.Slice(users, func(i, j int) bool { return users[i].id < users[j].id })
	sort.Slice(events, func(i, j int) bool { return events[i].id < events[j].id })

	joinedRows := make([]joined, 0, len(events))
	for i, j := 0, 0; i < len(users) && j < len(events); {
		if users[i].id < events[j].id {
			i++
		} else if users[i].id > events[j].id {
			j++
		} else {
			current := users[i]
			for j < len(events) && events[j].id == current.id {
				joinedRows = append(joinedRows, joined{
					region:    current.region,
					tier:      current.tier,
					latencyMS: events[j].latencyMS,
					bytes:     events[j].bytes,
				})
				j++
			}
			i++
		}
	}

	sort.Slice(joinedRows, func(i, j int) bool {
		if joinedRows[i].region != joinedRows[j].region {
			return joinedRows[i].region < joinedRows[j].region
		}
		return joinedRows[i].tier < joinedRows[j].tier
	})

	writer := bufio.NewWriterSize(os.Stdout, 1<<20)
	for i := 0; i < len(joinedRows); {
		row := joinedRows[i]
		count := int64(0)
		latencySum := int64(0)
		bytesSum := int64(0)
		for i < len(joinedRows) && joinedRows[i].region == row.region && joinedRows[i].tier == row.tier {
			count++
			latencySum += joinedRows[i].latencyMS
			bytesSum += joinedRows[i].bytes
			i++
		}
		fmt.Fprintf(writer, "%s,%s,%d,%d,%d\n", row.region, row.tier, count, latencySum, bytesSum)
	}
	writer.Flush()
}
