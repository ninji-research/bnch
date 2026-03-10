let line_width = 60

fn string_char_at(text : String, index : Int) -> Char {
  text[index].to_int().unsafe_to_char()
}

fn complement(ch : Char) -> Char {
  match ch.to_ascii_uppercase() {
    'A' => 'T'
    'C' => 'G'
    'G' => 'C'
    'T' => 'A'
    'U' => 'A'
    'M' => 'K'
    'R' => 'Y'
    'W' => 'W'
    'S' => 'S'
    'Y' => 'R'
    'K' => 'M'
    'V' => 'B'
    'H' => 'D'
    'D' => 'H'
    'B' => 'V'
    _ => 'N'
  }
}

fn array_prefix(chars : Array[Char], count : Int) -> String {
  let out = Array::make(count, 'A')
  for i = 0; i < count; i = i + 1 {
    out[i] = chars[i]
  }
  String::from_array(out)
}

fn flush_record(header : String, sequence : Array[Char]) -> Unit {
  if header.length() == 0 {
    return
  }
  println(header)
  let line = Array::make(line_width, 'A')
  let mut filled = 0
  for i = sequence.length() - 1; i >= 0; i = i - 1 {
    line[filled] = complement(sequence[i])
    filled = filled + 1
    if filled == line_width {
      println(String::from_array(line))
      filled = 0
    }
  }
  if filled > 0 {
    println(array_prefix(line, filled))
  }
}

fn process_line(line : String, current_header : String, current_seq : Array[Char]) -> (String, Array[Char]) {
  if line.length() == 0 {
    return (current_header, current_seq)
  }
  if string_char_at(line, 0) == '>' {
    flush_record(current_header, current_seq)
    return (line, Array::new())
  }
  for i = 0; i < line.length(); i = i + 1 {
    current_seq.push(string_char_at(line, i).to_ascii_uppercase())
  }
  (current_header, current_seq)
}

///| native stdin read via libc getchar
extern "c" fn getchar() -> Int = "getchar"

fn read_stdin() -> String {
  let sb = StringBuilder::new()
  while true {
    let code = getchar()
    if code < 0 {
      break
    }
    let ch = code.unsafe_to_char()
    if ch != '\r' {
      sb.write_char(ch)
    }
  }
  sb.to_string()
}

fn main {
  let input = read_stdin()
  let mut line = StringBuilder::new()
  let mut header = ""
  let mut sequence = Array::new()
  for _, ch in input {
    if ch == '\n' {
      let next = process_line(line.to_string(), header, sequence)
      header = next.0
      sequence = next.1
      line = StringBuilder::new()
    } else {
      line.write_char(ch)
    }
  }
  let next = process_line(line.to_string(), header, sequence)
  header = next.0
  sequence = next.1
  flush_record(header, sequence)
}
