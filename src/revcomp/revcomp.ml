let line_width = 60

let complement = function
  | 'A' | 'a' -> 'T'
  | 'C' | 'c' -> 'G'
  | 'G' | 'g' -> 'C'
  | 'T' | 't' -> 'A'
  | 'U' | 'u' -> 'A'
  | 'M' | 'm' -> 'K'
  | 'R' | 'r' -> 'Y'
  | 'W' | 'w' -> 'W'
  | 'S' | 's' -> 'S'
  | 'Y' | 'y' -> 'R'
  | 'K' | 'k' -> 'M'
  | 'V' | 'v' -> 'B'
  | 'H' | 'h' -> 'D'
  | 'D' | 'd' -> 'H'
  | 'B' | 'b' -> 'V'
  | _ -> 'N'

let flush_record header sequence =
  if header <> "" then begin
    print_endline header;
    let n = Buffer.length sequence in
    let text = Buffer.contents sequence in
    let line = Bytes.make line_width 'A' in
    let filled = ref 0 in
    for i = n - 1 downto 0 do
      Bytes.set line !filled (complement text.[i]);
      incr filled;
      if !filled = line_width then begin
        output stdout line 0 line_width;
        output_char stdout '\n';
        filled := 0
      end
    done;
    if !filled > 0 then begin
      output stdout line 0 !filled;
      output_char stdout '\n'
    end
  end

let () =
  let header = ref "" in
  let sequence = Buffer.create 262_144 in
  (try
     while true do
       let line = input_line stdin in
       if line <> "" then
         if line.[0] = '>' then begin
           flush_record !header sequence;
           header := line;
           Buffer.clear sequence
         end else
           String.iter (fun ch -> Buffer.add_char sequence (Char.uppercase_ascii ch)) line
     done
   with End_of_file -> ());
  flush_record !header sequence
