let () =
  let size = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 4000 in
  let inv_size = 2.0 /. float_of_int size in
  let sum = ref 0 in
  let iter = 50 in
  let limit = 4.0 in
  for y = 0 to size - 1 do
    let ci = float_of_int y *. inv_size -. 1.0 in
    for x = 0 to (size / 8) - 1 do
      let byte_val = ref 0 in
      for b = 0 to 7 do
        let cr = float_of_int (x * 8 + b) *. inv_size -. 1.5 in
        let zr = ref 0.0 in
        let zi = ref 0.0 in
        let tr = ref 0.0 in
        let ti = ref 0.0 in
        let i = ref 0 in
        while !i < iter && !tr +. !ti <= limit do
          zi := 2.0 *. !zr *. !zi +. ci;
          zr := !tr -. !ti +. cr;
          tr := !zr *. !zr;
          ti := !zi *. !zi;
          incr i
        done;
        if !tr +. !ti <= limit then
          byte_val := !byte_val lor (1 lsl (7 - b))
      done;
      sum := !sum + !byte_val
    done
  done;
  Printf.printf "%d\n" !sum
