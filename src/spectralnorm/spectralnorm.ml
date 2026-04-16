let eval_A i j = 1.0 /. float_of_int ((i + j) * (i + j + 1) / 2 + i + 1)

let eval_A_times_u u au =
  let n = Array.length u in
  for i = 0 to n - 1 do
    au.(i) <- 0.0;
    for j = 0 to n - 1 do
      au.(i) <- au.(i) +. eval_A i j *. u.(j)
    done
  done

let eval_At_times_u u au =
  let n = Array.length u in
  for i = 0 to n - 1 do
    au.(i) <- 0.0;
    for j = 0 to n - 1 do
      au.(i) <- au.(i) +. eval_A j i *. u.(j)
    done
  done

let eval_AtA_times_u u v w =
  eval_A_times_u u w;
  eval_At_times_u w v

let () =
  let n = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 5500 in
  let u = Array.make n 1.0 in
  let v = Array.make n 0.0 in
  let w = Array.make n 0.0 in
  for _i = 1 to 10 do
    eval_AtA_times_u u v w;
    eval_AtA_times_u v u w
  done;
  let vBv = ref 0.0 in
  let vv = ref 0.0 in
  for i = 0 to n - 1 do
    vBv := !vBv +. u.(i) *. v.(i);
    vv := !vv +. v.(i) *. v.(i)
  done;
  Printf.printf "%.9f\n" (sqrt (!vBv /. !vv))