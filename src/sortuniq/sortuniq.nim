import std/[algorithm, strutils]

when isMainModule:
  var words: seq[string] = @[]
  for rawLine in stdin.readAll().splitLines():
    let word = rawLine.strip(chars = {'\r'})
    if word.len != 0:
      words.add(word)

  words.sort(system.cmp[string])

  var current = ""
  var count = 0
  for word in words:
    if word != current:
      if current.len != 0:
        stdout.write(current & "," & $count & "\n")
      current = word
      count = 0
    inc count

  if current.len != 0:
    stdout.write(current & "," & $count & "\n")
