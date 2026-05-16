let is_prime n =
  if n < 2 then false
  else if n mod 2 = 0 then n = 2
  else begin
    let rec loop i =
      if n / i >= i then
        if n mod i = 0 then false
        else loop (i + 2)
      else true
    in
    loop 3
  end

let () =
  let n = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 50000 in
  let count = ref 0 in
  for i = 2 to n do
    if is_prime i then incr count
  done;
  Printf.printf "%d\n" !count
