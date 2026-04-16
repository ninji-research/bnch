let () =
  let words = ref [] in
  (try
     while true do
       let line = input_line stdin in
       if line <> "" then
         words := line :: !words
     done
   with End_of_file -> ());
  let words = Array.of_list !words in
  Array.sort String.compare words;
  let current = ref "" in
  let count = ref 0 in
  Array.iter
    (fun word ->
      if word <> !current then begin
        if !current <> "" then
          Printf.printf "%s,%d\n" !current !count;
        current := word;
        count := 0
      end;
      incr count)
    words;
  if !current <> "" then
    Printf.printf "%s,%d\n" !current !count
