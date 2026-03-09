let xorshift32 state =
  let x = !state in
  let x = Int32.logxor x (Int32.shift_left x 13) in
  let x = Int32.logxor x (Int32.shift_right_logical x 17) in
  let x = Int32.logxor x (Int32.shift_left x 5) in
  state := x;
  let unsigned =
    Int64.logand (Int64.of_int32 x) 0xFFFF_FFFFL
  in
  (Int64.to_float unsigned) /. 4294967295.0

let worker start_seed iterations =
  let state = ref (Int32.of_int start_seed) in
  let inside = ref 0 in
  for _ = 1 to iterations do
    let x = xorshift32 state in
    let y = xorshift32 state in
    if x *. x +. y *. y <= 1.0 then incr inside
  done;
  !inside

let () =
  let total_iters = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 50_000_000 in
  let num_threads =
    if Array.length Sys.argv > 2 then max 1 (int_of_string Sys.argv.(2)) else 4
  in
  
  let domains = Array.init num_threads (fun i ->
    let start = (total_iters * i) / num_threads in
    let finish = (total_iters * (i + 1)) / num_threads in
    Domain.spawn (fun () -> worker (12345 + i) (finish - start))
  ) in
  
  let total_inside = Array.fold_left (fun acc d -> acc + Domain.join d) 0 domains in
  let pi = 4.0 *. float_of_int total_inside /. float_of_int total_iters in
  Printf.printf "%.5f\n" pi
