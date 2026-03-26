import std/[algorithm, strutils]

type
  Row = tuple[customer: string, qty: int, cents: int]

proc parseRow(line: string): Row =
  let cols = line.split(',', maxsplit = 3)
  (cols[0], parseInt(cols[2]), parseInt(cols[3]))

when isMainModule:
  var rows: seq[Row] = @[]
  var first = true
  for rawLine in stdin.readAll().splitLines():
    let line = rawLine.strip(chars = {'\r'})
    if line.len == 0:
      continue
    if first:
      first = false
      continue
    rows.add(parseRow(line))

  rows.sort(proc(a, b: Row): int = cmp(a.customer, b.customer))

  var current = ""
  var count = 0
  var qtySum = 0
  var centsSum = 0
  for row in rows:
    if row.customer != current:
      if current.len != 0:
        stdout.write(current & "," & $count & "," & $qtySum & "," & $centsSum & "\n")
      current = row.customer
      count = 0
      qtySum = 0
      centsSum = 0
    inc count
    qtySum += row.qty
    centsSum += row.cents

  if current.len != 0:
    stdout.write(current & "," & $count & "," & $qtySum & "," & $centsSum & "\n")
