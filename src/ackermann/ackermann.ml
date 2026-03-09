let rec ackermann m n =
  if m = 0 then n + 1
  else if m > 0 && n = 0 then ackermann (m - 1) 1
  else ackermann (m - 1) (ackermann m (n - 1))
let () =
  let m = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 3 in
  let n = if Array.length Sys.argv > 2 then int_of_string Sys.argv.(2) else 11 in
  Printf.printf "%d\n" (ackermann m n)