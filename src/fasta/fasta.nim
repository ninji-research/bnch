import std/[os, strutils]

const
  LineWidth = 60
  Modulus = 139968
  Multiplier = 3877
  Increment = 29573
  Alu =
    "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" &
    "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA" &
    "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT" &
    "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA" &
    "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG" &
    "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC" &
    "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA"

type
  Freq = tuple[ch: char, p: float]

const
  Iub = [
    ('a', 0.27), ('c', 0.12), ('g', 0.12), ('t', 0.27), ('B', 0.02), ('D', 0.02), ('H', 0.02),
    ('K', 0.02), ('M', 0.02), ('N', 0.02), ('R', 0.02), ('S', 0.02), ('V', 0.02), ('W', 0.02), ('Y', 0.02),
  ]
  HomoSapiens = [
    ('a', 0.3029549426680), ('c', 0.1979883004921), ('g', 0.1975473066391), ('t', 0.3015094502008),
  ]

var rngState = 42

proc nextRandom(): float =
  rngState = (rngState * Multiplier + Increment) mod Modulus
  rngState.float / Modulus.float

proc emitRepeat(header, pattern: string; length: int) =
  stdout.write(">")
  stdout.write(header)
  stdout.write('\n')
  if length <= 0:
    return
  var line = newString(LineWidth)
  var index = 0
  var remaining = length
  while remaining > 0:
    let count = min(LineWidth, remaining)
    for i in 0..<count:
      line[i] = pattern[index]
      inc index
      if index == pattern.len:
        index = 0
    stdout.write(line[0 ..< count])
    stdout.write('\n')
    remaining -= count

proc emitRandom(header: string; table: openArray[Freq]; length: int) =
  stdout.write(">")
  stdout.write(header)
  stdout.write('\n')
  if length <= 0:
    return
  var cumulative = newSeq[Freq](table.len)
  var running = 0.0
  for i, entry in table:
    running += entry.p
    cumulative[i] = (entry.ch, running)

  var line = newString(LineWidth)
  var remaining = length
  while remaining > 0:
    let count = min(LineWidth, remaining)
    for i in 0..<count:
      let target = nextRandom()
      var chosen = cumulative[^1].ch
      for entry in cumulative:
        if target < entry.p:
          chosen = entry.ch
          break
      line[i] = chosen
    stdout.write(line[0 ..< count])
    stdout.write('\n')
    remaining -= count

when isMainModule:
  let n = if paramCount() > 0: parseInt(paramStr(1)) else: 250000
  emitRepeat("ONE Homo sapiens alu", Alu, n * 2)
  emitRandom("TWO IUB ambiguity codes", Iub, n * 3)
  emitRandom("THREE Homo sapiens frequency", HomoSapiens, n * 5)
