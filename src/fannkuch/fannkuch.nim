import std/[os, strutils]

proc fannkuch(n: int): (int, int) =
  var p = newSeq[int](n)
  for i in 0..<n: p[i] = i
  var q = newSeq[int](n)
  var s = newSeq[int](n)
  var sign = 1
  var maxFlips = 0
  var sum = 0
  while true:
    var q0 = p[0]
    if q0 != 0:
      for i in 1..<n: q[i] = p[i]
      var flips = 1
      while true:
        var i = 1
        var j = q0 - 1
        while i < j:
          swap(q[i], q[j])
          i.inc; j.dec
        let t = q[q0]
        q[q0] = q0
        q0 = t
        if q0 == 0: break
        flips.inc
      if flips > maxFlips: maxFlips = flips
      sum += sign * flips
    if sign == 1:
      swap(p[0], p[1])
      sign = -1
    else:
      swap(p[1], p[2])
      sign = 1
      for i in 2..<n:
        let sx = s[i]
        if sx < i:
          s[i] = sx + 1
          break
        s[i] = 0
        let t = p[0]
        for j in 0..<i: p[j] = p[j+1]
        p[i] = t
        if i == n - 1: return (sum, maxFlips)

let n = if paramCount() > 0: parseInt(paramStr(1)) else: 11
let (sum, maxFlips) = fannkuch(n)
echo sum
echo "Pfannkuchen(", n, ") = ", maxFlips
