let line_width = 60
let modulus = 139_968
let multiplier = 3_877
let increment = 29_573

let alu =
  "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG\
   GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA\
   CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT\
   ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA\
   GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG\
   AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC\
   AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA"

let iub = [
  ('a', 0.27); ('c', 0.12); ('g', 0.12); ('t', 0.27); ('B', 0.02); ('D', 0.02); ('H', 0.02);
  ('K', 0.02); ('M', 0.02); ('N', 0.02); ('R', 0.02); ('S', 0.02); ('V', 0.02); ('W', 0.02); ('Y', 0.02);
]

let homo_sapiens = [
  ('a', 0.3029549426680); ('c', 0.1979883004921); ('g', 0.1975473066391); ('t', 0.3015094502008);
]

let rng_state = ref 42

let next_random () =
  rng_state := (!rng_state * multiplier + increment) mod modulus;
  float_of_int !rng_state /. float_of_int modulus

let emit_repeat header pattern length =
  Printf.printf ">%s\n" header;
  let pattern_len = String.length pattern in
  let line = Bytes.make line_width 'A' in
  let index = ref 0 in
  let remaining = ref length in
  while !remaining > 0 do
    let count = min line_width !remaining in
    for i = 0 to count - 1 do
      Bytes.set line i pattern.[!index];
      incr index;
      if !index = pattern_len then index := 0
    done;
    output stdout line 0 count;
    output_char stdout '\n';
    remaining := !remaining - count
  done

let cumulative_table table =
  let running = ref 0.0 in
  List.map (fun (ch, weight) ->
    running := !running +. weight;
    (ch, !running)
  ) table

let emit_random header table length =
  Printf.printf ">%s\n" header;
  let cumulative = cumulative_table table in
  let line = Bytes.make line_width 'A' in
  let remaining = ref length in
  while !remaining > 0 do
    let count = min line_width !remaining in
    for i = 0 to count - 1 do
      let target = next_random () in
      let rec pick = function
        | [] -> 'a'
        | (ch, threshold) :: rest -> if target < threshold then ch else pick rest
      in
      Bytes.set line i (pick cumulative)
    done;
    output stdout line 0 count;
    output_char stdout '\n';
    remaining := !remaining - count
  done

let () =
  let n =
    if Array.length Sys.argv > 1 then int_of_string Sys.argv.(1) else 250_000
  in
  emit_repeat "ONE Homo sapiens alu" alu (n * 2);
  emit_random "TWO IUB ambiguity codes" iub (n * 3);
  emit_random "THREE Homo sapiens frequency" homo_sapiens (n * 5)
