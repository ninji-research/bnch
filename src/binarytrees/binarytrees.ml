type node = Leaf | Node of node * node

let rec make d =
  if d = 0 then Leaf
  else Node (make (d - 1), make (d - 1))

let rec check t =
  match t with
  | Leaf -> 1
  | Node (l, r) -> 1 + check l + check r

let () =
  let n = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 21 in
  let min_depth = 4 in
  let max_depth = max (min_depth + 2) n in
  let stretch_depth = max_depth + 1 in
  let c = check (make stretch_depth) in
  Printf.printf "stretch tree of depth %d\t check: %d\n" stretch_depth c;
  let long_lived_tree = make max_depth in
  let rec loop_depths d =
    if d <= max_depth then begin
      let niter = 1 lsl (max_depth - d + min_depth) in
      let c = ref 0 in
      for _i = 1 to niter do c := !c + check (make d) done;
      Printf.printf "%d\t trees of depth %d\t check: %d\n" niter d !c;
      loop_depths (d + 2)
    end
  in
  loop_depths min_depth;
  Printf.printf "long lived tree of depth %d\t check: %d\n" max_depth (check long_lived_tree)