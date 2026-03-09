package main

import (
	"fmt"
	"os"
	"strconv"
)

type node struct {
	left  *node
	right *node
}

func bottomUpTree(depth int) *node {
	if depth <= 0 {
		return &node{}
	}
	return &node{
		left:  bottomUpTree(depth - 1),
		right: bottomUpTree(depth - 1),
	}
}

func itemCheck(tree *node) uint32 {
	if tree.left == nil {
		return 1
	}
	return 1 + itemCheck(tree.left) + itemCheck(tree.right)
}

func main() {
	n := 21
	if len(os.Args) > 1 {
		if value, err := strconv.Atoi(os.Args[1]); err == nil {
			n = value
		}
	}

	minDepth := 4
	maxDepth := n
	if minDepth+2 > maxDepth {
		maxDepth = minDepth + 2
	}
	stretchDepth := maxDepth + 1

	stretchTree := bottomUpTree(stretchDepth)
	fmt.Printf("stretch tree of depth %d\t check: %d\n", stretchDepth, itemCheck(stretchTree))

	longLivedTree := bottomUpTree(maxDepth)
	for depth := minDepth; depth <= maxDepth; depth += 2 {
		iterations := 1 << (maxDepth - depth + minDepth)
		var check uint32
		for i := 0; i < iterations; i++ {
			check += itemCheck(bottomUpTree(depth))
		}
		fmt.Printf("%d\t trees of depth %d\t check: %d\n", iterations, depth, check)
	}

	fmt.Printf("long lived tree of depth %d\t check: %d\n", maxDepth, itemCheck(longLivedTree))
}
