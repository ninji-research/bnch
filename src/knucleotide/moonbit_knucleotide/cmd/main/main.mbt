fn encode_base(ch : Char) -> Int {
  match ch {
    'A' => 0
    'C' => 1
    'G' => 2
    'T' => 3
    _ => -1
  }
}

fn string_char_at(text : String, index : Int) -> Char {
  text[index].to_int().unsafe_to_char()
}

fn char_from_code(code : Int) -> Char {
  match code {
    0 => 'A'
    1 => 'C'
    2 => 'G'
    _ => 'T'
  }
}

fn code_to_string(code : Int, k : Int) -> String {
  let chars = Array::make(k, 'A')
  let mut value = code
  for i = k - 1; i >= 0; i = i - 1 {
    chars[i] = char_from_code(value & 3)
    value = value >> 2
  }
  String::from_array(chars)
}

fn starts_with_three(line : String) -> Bool {
  line.length() >= 6 &&
  string_char_at(line, 0) == '>' &&
  string_char_at(line, 1) == 'T' &&
  string_char_at(line, 2) == 'H' &&
  string_char_at(line, 3) == 'R' &&
  string_char_at(line, 4) == 'E' &&
  string_char_at(line, 5) == 'E'
}

fn parse_sequence(text : String) -> Array[Int] {
  let seq = Array::new()
  let mut line = StringBuilder::new()
  let mut capture = false

  fn process_line(line_text : String, capture_ref : Bool, seq : Array[Int]) -> Bool {
    if line_text.length() == 0 {
      return capture_ref
    }
    if string_char_at(line_text, 0) == '>' {
      if capture_ref {
        return false
      }
      return starts_with_three(line_text)
    }
    if capture_ref {
      for i = 0; i < line_text.length(); i = i + 1 {
        let code = encode_base(string_char_at(line_text, i).to_ascii_uppercase())
        if code >= 0 {
          seq.push(code)
        }
      }
    }
    capture_ref
  }

  for _, ch in text {
    if ch == '\n' {
      capture = process_line(line.to_string(), capture, seq)
      line = StringBuilder::new()
    } else if ch != '\r' {
      line.write_char(ch)
    }
  }
  capture = process_line(line.to_string(), capture, seq)
  ignore(capture)
  seq
}

fn pad3(n : Int) -> String {
  if n < 10 {
    "00" + n.to_string()
  } else if n < 100 {
    "0" + n.to_string()
  } else {
    n.to_string()
  }
}

fn format_percent(count : Int, total : Int) -> String {
  let scaled = ((count.to_double() * 100000.0 / total.to_double()) + 0.5).to_int()
  let whole = scaled / 1000
  let frac = scaled % 1000
  whole.to_string() + "." + pad3(frac)
}

fn frequency_lines(seq : Array[Int], k : Int) -> Array[String] {
  if seq.length() < k {
    return []
  }
  let bucket_count = 1 << (2 * k)
  let counts = Array::make(bucket_count, 0)
  let total = seq.length() - k + 1
  let mask = bucket_count - 1
  let mut rolling = 0
  for i = 0; i < k; i = i + 1 {
    rolling = (rolling << 2) | seq[i]
  }
  counts[rolling] = counts[rolling] + 1
  for i = k; i < seq.length(); i = i + 1 {
    rolling = ((rolling << 2) & mask) | seq[i]
    counts[rolling] = counts[rolling] + 1
  }
  let entries = Array::new()
  for code = 0; code < bucket_count; code = code + 1 {
    let count = counts[code]
    if count > 0 {
      entries.push((code_to_string(code, k), count))
    }
  }
  for i = 0; i < entries.length(); i = i + 1 {
    for j = i + 1; j < entries.length(); j = j + 1 {
      let a = entries[i]
      let b = entries[j]
      if b.1 > a.1 || (b.1 == a.1 && b.0 < a.0) {
        entries[i] = b
        entries[j] = a
      }
    }
  }
  let out = Array::new()
  for i = 0; i < entries.length(); i = i + 1 {
    let entry = entries[i]
    out.push(entry.0 + " " + format_percent(entry.1, total))
  }
  out
}

fn count_fragment(seq : Array[Int], target : String) -> Int {
  if seq.length() < target.length() {
    return 0
  }
  let encoded = Array::make(target.length(), 0)
  for i = 0; i < target.length(); i = i + 1 {
    encoded[i] = encode_base(string_char_at(target, i))
  }
  let mut count = 0
  for i = 0; i <= seq.length() - target.length(); i = i + 1 {
    let mut ok = true
    for j = 0; j < target.length(); j = j + 1 {
      if seq[i + j] != encoded[j] {
        ok = false
        break
      }
    }
    if ok {
      count = count + 1
    }
  }
  count
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
    sb.write_char(code.unsafe_to_char())
  }
  sb.to_string()
}

fn main {
  let input = read_stdin()
  let seq = parse_sequence(input)
  let mono = frequency_lines(seq, 1)
  for i = 0; i < mono.length(); i = i + 1 {
    println(mono[i])
  }
  println("")
  let di = frequency_lines(seq, 2)
  for i = 0; i < di.length(); i = i + 1 {
    println(di[i])
  }
  println("")
  let targets = [
    "GGT",
    "GGTA",
    "GGTATT",
    "GGTATTTTAATT",
    "GGTATTTTAATTTATAGT",
  ]
  for i = 0; i < targets.length(); i = i + 1 {
    let target = targets[i]
    println(count_fragment(seq, target).to_string() + "\t" + target)
  }
}
