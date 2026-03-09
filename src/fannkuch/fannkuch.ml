let fannkuch n =
  let p = Array.init n (fun i -> i) in
  let q = Array.make n 0 in
  let s = Array.make n 0 in
  let sign = ref 1 in
  let max_flips = ref 0 in
  let sum = ref 0 in
  let rec loop () =
    let q0 = ref p.(0) in
    if !q0 <> 0 then begin
      for i = 1 to n - 1 do q.(i) <- p.(i) done;
      let flips = ref 1 in
      let rec flip_loop q0_val =
        let i = ref 1 in
        let j = ref (q0_val - 1) in
        while !i < !j do
          let t = q.(!i) in q.(!i) <- q.(!j); q.(!j) <- t;
          incr i; decr j
        done;
        let t = q.(q0_val) in
        q.(q0_val) <- q0_val;
        if t = 0 then !flips
        else (incr flips; flip_loop t)
      in
      let f = flip_loop !q0 in
      if f > !max_flips then max_flips := f;
      sum := !sum + !sign * f
    end;
    if !sign = 1 then begin
      let t = p.(0) in p.(0) <- p.(1); p.(1) <- t;
      sign := -1; loop ()
    end else begin
      let t = p.(1) in p.(1) <- p.(2); p.(2) <- t;
      sign := 1;
      let rec yield_loop i =
        if i = n then (!sum, !max_flips)
        else
          let sx = s.(i) in
          if sx < i then begin
            s.(i) <- sx + 1;
            loop ()
          end else begin
            s.(i) <- 0;
            let t = p.(0) in
            for j = 0 to i - 1 do p.(j) <- p.(j+1) done;
            p.(i) <- t;
            yield_loop (i + 1)
          end
      in yield_loop 2
    end
  in loop ()

let () =
  let n = if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 11 in
  let sum, max_flips = fannkuch n in
  Printf.printf "%d\nPfannkuchen(%d) = %d\n" sum n max_flips
