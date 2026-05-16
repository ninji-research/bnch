import std/[os, strutils]

proc isPrime(n: int): bool =
  if n < 2: return false
  if n mod 2 == 0: return n == 2
  var i = 3
  while n div i >= i:
    if n mod i == 0: return false
    i += 2
  true

proc main() =
  let n = if paramCount() > 0: parseInt(paramStr(1)) else: 50000
  var count = 0
  for i in 2..n:
    if isPrime(i): inc count
  echo count

main()
