import std/[os, strutils]
proc ackermann(m, n: int): int =
  if m == 0: n + 1
  elif m > 0 and n == 0: ackermann(m - 1, 1)
  else: ackermann(m - 1, ackermann(m, n - 1))
let m = if paramCount() > 0: parseInt(paramStr(1)) else: 3
let n = if paramCount() > 1: parseInt(paramStr(2)) else: 11
echo ackermann(m, n)