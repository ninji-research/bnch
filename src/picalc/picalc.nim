import std/[os, strutils, threadpool]

proc xorshift32(state: var uint32): float64 =
  var x = state
  x = x xor (x shl 13)
  x = x xor (x shr 17)
  x = x xor (x shl 5)
  state = x
  return float64(x) / 4294967295.0

proc worker(start_seed: uint32, iterations: int): int =
  var state = start_seed
  var inside = 0
  for i in 0..<iterations:
    let x = xorshift32(state)
    let y = xorshift32(state)
    if x * x + y * y <= 1.0:
      inside.inc
  return inside

proc main() =
  let totalIters = if paramCount() > 0: parseInt(paramStr(1)) else: 50_000_000
  let numThreads = if paramCount() > 1: max(1, parseInt(paramStr(2))) else: 4
  
  var responses: seq[FlowVar[int]]
  for i in 0..<numThreads:
    let start = (totalIters * i) div numThreads
    let finish = (totalIters * (i + 1)) div numThreads
    responses.add(spawn worker(12345'u32 + uint32(i), finish - start))
    
  var totalInside = 0
  for i in 0..<numThreads:
    totalInside += ^responses[i]
    
  let pi = 4.0 * float64(totalInside) / float64(totalIters)
  echo formatFloat(pi, ffDecimal, 5)

main()
