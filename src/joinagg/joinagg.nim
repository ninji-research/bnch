import std/[algorithm, strutils]

type
  User = tuple[id: string, region: string, tier: string]
  Event = tuple[id: string, latencyMs: int, bytes: int]
  Joined = tuple[region: string, tier: string, latencyMs: int, bytes: int]

proc parseUser(line: string): User =
  let cols = line.split(',', maxsplit = 3)
  (cols[0], cols[1], cols[2])

proc parseEvent(line: string): Event =
  let cols = line.split(',', maxsplit = 3)
  (cols[0], parseInt(cols[2]), parseInt(cols[3]))

when isMainModule:
  var users: seq[User] = @[]
  var events: seq[Event] = @[]
  var section = ""
  var headerPending = false

  for rawLine in stdin.readAll().splitLines():
    let line = rawLine.strip(chars = {'\r'})
    if line.len == 0:
      continue
    if line == "[users]" or line == "[events]":
      section = line
      headerPending = true
      continue
    if headerPending:
      headerPending = false
      continue
    if section == "[users]":
      let cols = line.split(',', maxsplit = 3)
      if cols[3] == "active":
        users.add((cols[0], cols[1], cols[2]))
    elif section == "[events]":
      let cols = line.split(',', maxsplit = 3)
      if cols[1] != "noop":
        events.add((cols[0], parseInt(cols[2]), parseInt(cols[3])))

  users.sort(proc(a, b: User): int = cmp(a.id, b.id))
  events.sort(proc(a, b: Event): int = cmp(a.id, b.id))

  var joined: seq[Joined] = @[]
  var i = 0
  var j = 0
  while i < users.len and j < events.len:
    if users[i].id < events[j].id:
      inc i
    elif users[i].id > events[j].id:
      inc j
    else:
      let user = users[i]
      while j < events.len and events[j].id == user.id:
        joined.add((user.region, user.tier, events[j].latencyMs, events[j].bytes))
        inc j
      inc i

  joined.sort(proc(a, b: Joined): int =
    let regionCmp = cmp(a.region, b.region)
    if regionCmp != 0: regionCmp else: cmp(a.tier, b.tier)
  )

  var currentRegion = ""
  var currentTier = ""
  var count = 0
  var latencySum = 0
  var bytesSum = 0

  for row in joined:
    if row.region != currentRegion or row.tier != currentTier:
      if currentRegion.len != 0:
        stdout.write(currentRegion & "," & currentTier & "," & $count & "," & $latencySum & "," & $bytesSum & "\n")
      currentRegion = row.region
      currentTier = row.tier
      count = 0
      latencySum = 0
      bytesSum = 0
    inc count
    latencySum += row.latencyMs
    bytesSum += row.bytes

  if currentRegion.len != 0:
    stdout.write(currentRegion & "," & currentTier & "," & $count & "," & $latencySum & "," & $bytesSum & "\n")
