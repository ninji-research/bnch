type row = {
  customer : string;
  qty : int;
  cents : int;
}

let split_four line =
  let first = String.index line ',' in
  let second = String.index_from line (first + 1) ',' in
  let third = String.index_from line (second + 1) ',' in
  ( String.sub line 0 first,
    String.sub line (first + 1) (second - first - 1),
    String.sub line (second + 1) (third - second - 1),
    String.sub line (third + 1) (String.length line - third - 1) )

let parse_row line =
  let customer, _, qty, cents = split_four line in
  {
    customer;
    qty = int_of_string qty;
    cents = int_of_string cents;
  }

let () =
  let rows = ref [] in
  let first = ref true in
  (try
     while true do
       let line = input_line stdin in
       if line <> "" then begin
         if !first then
           first := false
         else
           rows := parse_row line :: !rows
       end
     done
   with End_of_file -> ());
  let rows = Array.of_list !rows in
  Array.sort (fun a b -> String.compare a.customer b.customer) rows;
  let current = ref "" in
  let count = ref 0 in
  let qty_sum = ref 0 in
  let cents_sum = ref 0 in
  Array.iter (fun row ->
    if row.customer <> !current then begin
      if !current <> "" then
        Printf.printf "%s,%d,%d,%d\n" !current !count !qty_sum !cents_sum;
      current := row.customer;
      count := 0;
      qty_sum := 0;
      cents_sum := 0
    end;
    incr count;
    qty_sum := !qty_sum + row.qty;
    cents_sum := !cents_sum + row.cents
  ) rows;
  if !current <> "" then
    Printf.printf "%s,%d,%d,%d\n" !current !count !qty_sum !cents_sum
