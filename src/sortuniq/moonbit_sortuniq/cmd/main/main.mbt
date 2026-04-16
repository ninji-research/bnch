fn merge(left : Array[String], right : Array[String]) -> Array[String] {
  let out = Array::new()
  let mut i = 0
  let mut j = 0
  while i < left.length() && j < right.length() {
    if left[i].lexical_compare(right[j]) <= 0 {
      out.push(left[i])
      i = i + 1
    } else {
      out.push(right[j])
      j = j + 1
    }
  }
  while i < left.length() {
    out.push(left[i])
    i = i + 1
  }
  while j < right.length() {
    out.push(right[j])
    j = j + 1
  }
  out
}

fn merge_sort(words : Array[String]) -> Array[String] {
  if words.length() <= 1 {
    return words
  }
  let mid = words.length() / 2
  let left = Array::new()
  let right = Array::new()
  for i = 0; i < mid; i = i + 1 {
    left.push(words[i])
  }
  for i = mid; i < words.length(); i = i + 1 {
    right.push(words[i])
  }
  merge(merge_sort(left), merge_sort(right))
}

fn emit_counts(words : Array[String]) -> Unit {
  let sorted = merge_sort(words)
  let mut current = ""
  let mut count = 0
  for i = 0; i < sorted.length(); i = i + 1 {
    let word = sorted[i]
    if word != current {
      if current.length() != 0 {
        println(current + "," + count.to_string())
      }
      current = word
      count = 0
    }
    count = count + 1
  }
  if current.length() != 0 {
    println(current + "," + count.to_string())
  }
}

fn process_line(line : String, words : Array[String]) -> Unit {
  if line.length() != 0 {
    words.push(line)
  }
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
  let words = Array::new()
  let mut line = StringBuilder::new()
  for _, ch in input {
    if ch == '\n' {
      process_line(line.to_string(), words)
      line = StringBuilder::new()
    } else {
      line.write_char(ch)
    }
  }
  process_line(line.to_string(), words)
  emit_counts(words)
}
