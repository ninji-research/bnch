let line_width = 60
let modulus = 139968
let multiplier = 3877
let increment = 29573

fn arg_or(index : Int, fallback : Int) -> Int {
  let args = @env.args()
  if args.length() > index {
    @strconv.parse_int(args[index]) catch {
      _ => fallback
    }
  } else {
    fallback
  }
}

fn string_char_at(text : String, index : Int) -> Char {
  text[index].to_int().unsafe_to_char()
}

fn array_prefix(chars : Array[Char], count : Int) -> String {
  let out = Array::make(count, 'A')
  for i = 0; i < count; i = i + 1 {
    out[i] = chars[i]
  }
  String::from_array(out)
}

fn next_random(state : Int) -> (Int, Double) {
  let next = (state * multiplier + increment) % modulus
  (next, next.to_double() / modulus.to_double())
}

fn write_repeat(header : String, pattern : String, length : Int) -> Unit {
  println(">" + header)
  if length <= 0 {
    return
  }
  let chars = Array::make(line_width, 'A')
  let mut index = 0
  let mut remaining = length
  while remaining > 0 {
    let count = if remaining < line_width { remaining } else { line_width }
    for i = 0; i < count; i = i + 1 {
      chars[i] = string_char_at(pattern, index)
      index = index + 1
      if index == pattern.length() {
        index = 0
      }
    }
    println(array_prefix(chars, count))
    remaining = remaining - count
  }
}

fn cumulative_table(table : Array[(Char, Double)]) -> Array[(Char, Double)] {
  let out = Array::new()
  let mut running = 0.0
  for i = 0; i < table.length(); i = i + 1 {
    let entry = table[i]
    running = running + entry.1
    out.push((entry.0, running))
  }
  out
}

fn write_random(header : String, table : Array[(Char, Double)], length : Int, seed : Int) -> Int {
  println(">" + header)
  if length <= 0 {
    return seed
  }
  let cumulative = cumulative_table(table)
  let chars = Array::make(line_width, 'a')
  let mut state = seed
  let mut remaining = length
  while remaining > 0 {
    let count = if remaining < line_width { remaining } else { line_width }
    for i = 0; i < count; i = i + 1 {
      let next = next_random(state)
      state = next.0
      let target = next.1
      let mut chosen = cumulative[cumulative.length() - 1].0
      for j = 0; j < cumulative.length(); j = j + 1 {
        let entry = cumulative[j]
        if target < entry.1 {
          chosen = entry.0
          break
        }
      }
      chars[i] = chosen
    }
    println(array_prefix(chars, count))
    remaining = remaining - count
  }
  state
}

fn main {
  let n = arg_or(1, 250000)
  let alu =
    "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" +
    "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA" +
    "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT" +
    "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA" +
    "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG" +
    "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC" +
    "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA"
  let iub = [
    ('a', 0.27), ('c', 0.12), ('g', 0.12), ('t', 0.27), ('B', 0.02), ('D', 0.02), ('H', 0.02),
    ('K', 0.02), ('M', 0.02), ('N', 0.02), ('R', 0.02), ('S', 0.02), ('V', 0.02), ('W', 0.02), ('Y', 0.02),
  ]
  let homo = [
    ('a', 0.3029549426680), ('c', 0.1979883004921), ('g', 0.1975473066391), ('t', 0.3015094502008),
  ]
  write_repeat("ONE Homo sapiens alu", alu, n * 2)
  let seed = write_random("TWO IUB ambiguity codes", iub, n * 3, 42)
  ignore(write_random("THREE Homo sapiens frequency", homo, n * 5, seed))
}
