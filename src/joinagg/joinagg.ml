type user = {
  id : string;
  region : string;
  tier : string;
}

type event = {
  id : string;
  latency_ms : int;
  bytes : int;
}

type joined = {
  region : string;
  tier : string;
  latency_ms : int;
  bytes : int;
}

let split_four line =
  let first = String.index line ',' in
  let second = String.index_from line (first + 1) ',' in
  let third = String.index_from line (second + 1) ',' in
  ( String.sub line 0 first,
    String.sub line (first + 1) (second - first - 1),
    String.sub line (second + 1) (third - second - 1),
    String.sub line (third + 1) (String.length line - third - 1) )

let () =
  let users = ref [] in
  let events = ref [] in
  let section = ref "" in
  let header_pending = ref false in
  (try
     while true do
       let line = input_line stdin in
       if line <> "" then begin
         if line = "[users]" || line = "[events]" then begin
           section := line;
           header_pending := true
         end else if !header_pending then
           header_pending := false
         else if !section = "[users]" then begin
           let id, region, tier, status = split_four line in
           if status = "active" then
             users := { id; region; tier } :: !users
         end else if !section = "[events]" then begin
           let id, kind, latency_ms, bytes = split_four line in
           if kind <> "noop" then
             events :=
               { id; latency_ms = int_of_string latency_ms; bytes = int_of_string bytes } :: !events
         end
       end
     done
   with End_of_file -> ());
  let users = Array.of_list !users in
  let events = Array.of_list !events in
  Array.sort (fun (a : user) (b : user) -> String.compare a.id b.id) users;
  Array.sort (fun (a : event) (b : event) -> String.compare a.id b.id) events;
  let joined = ref [] in
  let i = ref 0 in
  let j = ref 0 in
  while !i < Array.length users && !j < Array.length events do
    let user = users.(!i) in
    let event = events.(!j) in
    let cmp = String.compare user.id event.id in
    if cmp < 0 then
      incr i
    else if cmp > 0 then
      incr j
    else begin
      while !j < Array.length events && events.(!j).id = user.id do
        joined :=
          {
            region = user.region;
            tier = user.tier;
            latency_ms = events.(!j).latency_ms;
            bytes = events.(!j).bytes;
          }
          :: !joined;
        incr j
      done;
      incr i
    end
  done;
  let joined = Array.of_list !joined in
  Array.sort
    (fun a b ->
      let region_cmp = String.compare a.region b.region in
      if region_cmp <> 0 then region_cmp else String.compare a.tier b.tier)
    joined;
  let current_region = ref "" in
  let current_tier = ref "" in
  let count = ref 0 in
  let latency_sum = ref 0 in
  let bytes_sum = ref 0 in
  Array.iter
    (fun row ->
      if row.region <> !current_region || row.tier <> !current_tier then begin
        if !current_region <> "" then
          Printf.printf "%s,%s,%d,%d,%d\n" !current_region !current_tier !count !latency_sum !bytes_sum;
        current_region := row.region;
        current_tier := row.tier;
        count := 0;
        latency_sum := 0;
        bytes_sum := 0
      end;
      incr count;
      latency_sum := !latency_sum + row.latency_ms;
      bytes_sum := !bytes_sum + row.bytes)
    joined;
  if !current_region <> "" then
    Printf.printf "%s,%s,%d,%d,%d\n" !current_region !current_tier !count !latency_sum !bytes_sum
