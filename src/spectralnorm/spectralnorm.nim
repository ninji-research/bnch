import std/os, std/strutils, std/math

proc eval_A(i, j: int): float =
  return 1.0 / float((i + j) * (i + j + 1) div 2 + i + 1)

proc eval_A_times_u(u: openArray[float], au: var openArray[float]) =
  let n = u.len
  for i in 0 ..< n:
    au[i] = 0.0
    for j in 0 ..< n:
      au[i] += eval_A(i, j) * u[j]

proc eval_At_times_u(u: openArray[float], au: var openArray[float]) =
  let n = u.len
  for i in 0 ..< n:
    au[i] = 0.0
    for j in 0 ..< n:
      au[i] += eval_A(j, i) * u[j]

proc eval_AtA_times_u(u: openArray[float], v: var openArray[float], w: var openArray[float]) =
  eval_A_times_u(u, w)
  eval_At_times_u(w, v)

proc main() =
  let n = if paramCount() > 0: parseInt(paramStr(1)) else: 5500
  var u = newSeq[float](n)
  var v = newSeq[float](n)
  var w = newSeq[float](n)
  for i in 0 ..< n: u[i] = 1.0
  
  for i in 0 ..< 10:
    eval_AtA_times_u(u, v, w)
    eval_AtA_times_u(v, u, w)
    
  var vBv = 0.0
  var vv = 0.0
  for i in 0 ..< n:
    vBv += u[i] * v[i]
    vv += v[i] * v[i]
    
  echo formatFloat(sqrt(vBv / vv), ffDecimal, 9)

main()