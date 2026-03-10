import std/strutils

const LineWidth = 60

proc complement(ch: char): char =
  case ch.toUpperAscii()
  of 'A': 'T'
  of 'C': 'G'
  of 'G': 'C'
  of 'T': 'A'
  of 'U': 'A'
  of 'M': 'K'
  of 'R': 'Y'
  of 'W': 'W'
  of 'S': 'S'
  of 'Y': 'R'
  of 'K': 'M'
  of 'V': 'B'
  of 'H': 'D'
  of 'D': 'H'
  of 'B': 'V'
  else: 'N'

proc flushRecord(header: string; sequence: string) =
  if header.len == 0:
    return
  stdout.write(header)
  stdout.write('\n')
  var line = newString(LineWidth)
  var filled = 0
  for i in countdown(sequence.len - 1, 0):
    line[filled] = complement(sequence[i])
    inc filled
    if filled == LineWidth:
      stdout.write(line)
      stdout.write('\n')
      filled = 0
  if filled > 0:
    stdout.write(line[0 ..< filled])
    stdout.write('\n')

when isMainModule:
  var header = ""
  var sequence = newStringOfCap(262144)
  for rawLine in stdin.readAll().splitLines():
    let line = rawLine.strip(chars = {'\r'})
    if line.len == 0:
      continue
    if line[0] == '>':
      flushRecord(header, sequence)
      header = line
      sequence.setLen(0)
    else:
      for ch in line:
        sequence.add(ch.toUpperAscii())
  flushRecord(header, sequence)
