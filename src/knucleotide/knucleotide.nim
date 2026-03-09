import std/[algorithm, strformat, strutils]

const Targets = [
  "GGT",
  "GGTA",
  "GGTATT",
  "GGTATTTTAATT",
  "GGTATTTTAATTTATAGT",
]

proc extractSequence(text: string): string =
  var capture = false
  for rawLine in text.splitLines():
    let line = rawLine.strip()
    if line.len == 0:
      continue
    if line[0] == '>':
      if capture:
        break
      capture = line.startsWith(">THREE")
      continue
    if capture:
      for ch in line:
        result.add(ch.toUpperAscii())

proc encodeBase(ch: char): int =
  case ch
  of 'A': 0
  of 'C': 1
  of 'G': 2
  of 'T': 3
  else: -1

proc codeToString(code: int; k: int): string =
  result = newString(k)
  var value = code
  for i in countdown(k - 1, 0):
    result[i] = case value and 3
      of 0: 'A'
      of 1: 'C'
      of 2: 'G'
      else: 'T'
    value = value shr 2

proc frequencyBlock(sequence: string; k: int): string =
  if sequence.len < k:
    return ""
  let bucketCount = 1 shl (2 * k)
  var counts = newSeq[int](bucketCount)
  var total = sequence.len - k + 1
  let mask = bucketCount - 1
  var rolling = 0
  for i in 0..<k:
    rolling = (rolling shl 2) or encodeBase(sequence[i])
  counts[rolling].inc()
  for i in k..<sequence.len:
    rolling = ((rolling shl 2) and mask) or encodeBase(sequence[i])
    counts[rolling].inc()

  var entries: seq[(string, int)] = @[]
  for code, count in counts:
    if count > 0:
      entries.add((codeToString(code, k), count))
  entries.sort(proc(a, b: (string, int)): int =
    if a[1] != b[1]:
      cmp(b[1], a[1])
    else:
      cmp(a[0], b[0])
  )

  for i, entry in entries:
    if i > 0:
      result.add('\n')
    result.add(&"{entry[0]} {100.0 * float(entry[1]) / float(total):.3f}")

proc countFragment(sequence, target: string): int =
  let limit = sequence.len - target.len
  if limit < 0:
    return 0
  for i in 0..limit:
    if sequence.continuesWith(target, i):
      result.inc()

when isMainModule:
  let sequence = extractSequence(stdin.readAll())
  stdout.write(frequencyBlock(sequence, 1))
  stdout.write("\n\n")
  stdout.write(frequencyBlock(sequence, 2))
  stdout.write("\n\n")
  for target in Targets:
    stdout.write($countFragment(sequence, target))
    stdout.write('\t')
    stdout.write(target)
    stdout.write('\n')
