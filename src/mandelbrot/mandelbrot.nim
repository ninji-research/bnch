import std/os, std/strutils
proc main() =
  let size = if paramCount() > 0: parseInt(paramStr(1)) else: 4000
  let invSize = 2.0 / size.float
  var sum = 0
  for y in 0 ..< size:
    let ci = y.float * invSize - 1.0
    for x in 0 ..< (size div 8):
      var byteVal = 0
      for b in 0 .. 7:
        let cr = (x * 8 + b).float * invSize - 1.5
        var zr = 0.0
        var zi = 0.0
        var tr = 0.0
        var ti = 0.0
        var i = 0
        while i < 50 and tr + ti <= 4.0:
          zi = 2.0 * zr * zi + ci
          zr = tr - ti + cr
          tr = zr * zr
          ti = zi * zi
          i += 1
        if tr + ti <= 4.0:
          byteVal = byteVal or (1 shl (7 - b))
      sum += byteVal
  echo sum
main()
