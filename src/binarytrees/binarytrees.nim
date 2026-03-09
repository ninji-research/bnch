import std/os, std/strutils

type
  Node = ref object
    left, right: Node

proc itemCheck(n: Node): int =
  if n.left == nil: 1
  else: 1 + itemCheck(n.left) + itemCheck(n.right)

proc bottomUpTree(depth: int): Node =
  if depth > 0:
    Node(left: bottomUpTree(depth - 1), right: bottomUpTree(depth - 1))
  else:
    Node(left: nil, right: nil)

proc main() =
  let n = if paramCount() > 0: parseInt(paramStr(1)) else: 21
  let minDepth = 4
  let maxDepth = if minDepth + 2 > n: minDepth + 2 else: n
  let stretchDepth = maxDepth + 1
  
  let stretchTree = bottomUpTree(stretchDepth)
  echo "stretch tree of depth ", stretchDepth, "\t check: ", itemCheck(stretchTree)
  
  let longLivedTree = bottomUpTree(maxDepth)
  
  var depth = minDepth
  while depth <= maxDepth:
    let iterations = 1 shl (maxDepth - depth + minDepth)
    var check = 0
    for i in 1..iterations:
      check += itemCheck(bottomUpTree(depth))
    echo iterations, "\t trees of depth ", depth, "\t check: ", check
    depth += 2
    
  echo "long lived tree of depth ", maxDepth, "\t check: ", itemCheck(longLivedTree)

main()