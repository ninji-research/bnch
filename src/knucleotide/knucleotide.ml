let targets = [
  "GGT";
  "GGTA";
  "GGTATT";
  "GGTATTTTAATT";
  "GGTATTTTAATTTATAGT";
]

let extract_sequence text =
  let len = String.length text in
  let buffer = Buffer.create len in
  let rec scan_line_start i capture =
    if i >= len then ()
    else
      let j =
        match String.index_from_opt text i '\n' with
        | Some idx -> idx
        | None -> len
      in
      let line_len = j - i in
      if line_len > 0 && text.[i] = '>' then
        if capture then ()
        else
          let next_capture =
            line_len >= 6 &&
            String.sub text i 6 = ">THREE"
          in
          scan_line_start (if j < len then j + 1 else j) next_capture
      else begin
        if capture then
          for k = i to j - 1 do
            Buffer.add_char buffer (Char.uppercase_ascii text.[k])
          done;
        scan_line_start (if j < len then j + 1 else j) capture
      end
  in
  scan_line_start 0 false;
  Buffer.contents buffer

let encode_base = function
  | 'A' -> 0
  | 'C' -> 1
  | 'G' -> 2
  | 'T' -> 3
  | _ -> -1

let code_to_string code k =
  let out = Bytes.make k 'A' in
  let value = ref code in
  for i = k - 1 downto 0 do
    Bytes.set out i
      (match !value land 3 with
      | 0 -> 'A'
      | 1 -> 'C'
      | 2 -> 'G'
      | _ -> 'T');
    value := !value lsr 2
  done;
  Bytes.unsafe_to_string out

let frequency_block sequence k =
  let n = String.length sequence in
  if n < k then ""
  else
    let bucket_count = 1 lsl (2 * k) in
    let counts = Array.make bucket_count 0 in
    let total = n - k + 1 in
    let mask = bucket_count - 1 in
    let rolling = ref 0 in
    for i = 0 to k - 1 do
      rolling := (!rolling lsl 2) lor encode_base sequence.[i]
    done;
    counts.(!rolling) <- counts.(!rolling) + 1;
    for i = k to n - 1 do
      rolling := ((!rolling lsl 2) land mask) lor encode_base sequence.[i];
      counts.(!rolling) <- counts.(!rolling) + 1
    done;
    let entries = ref [] in
    Array.iteri (fun code count ->
      if count > 0 then entries := (code_to_string code k, count) :: !entries
    ) counts;
    let sorted =
      List.sort (fun (sa, ca) (sb, cb) ->
        let by_count = compare cb ca in
        if by_count <> 0 then by_count else compare sa sb
      ) !entries
    in
    String.concat "\n" (
      List.map (fun (fragment, count) ->
        Printf.sprintf "%s %.3f" fragment (100.0 *. float_of_int count /. float_of_int total)
      ) sorted
    )

let count_fragment sequence target =
  let n = String.length sequence in
  let m = String.length target in
  let count = ref 0 in
  for i = 0 to n - m do
    if String.sub sequence i m = target then incr count
  done;
  !count

let () =
  let sequence = extract_sequence (In_channel.input_all In_channel.stdin) in
  print_endline (frequency_block sequence 1);
  print_newline ();
  print_endline (frequency_block sequence 2);
  print_newline ();
  List.iter (fun target ->
    Printf.printf "%d\t%s\n" (count_fragment sequence target) target
  ) targets
