fn parse_row(line : String) -> (String, Int, Int) {
  let customer = StringBuilder::new()
  let mut field = 0
  let mut qty = 0
  let mut cents = 0
  for _, ch in line {
    if ch == ',' {
      field = field + 1
    } else if field == 0 {
      customer.write_char(ch)
    } else if field == 2 {
      qty = (qty * 10) + ch.to_int() - '0'.to_int()
    } else if field == 3 {
      cents = (cents * 10) + ch.to_int() - '0'.to_int()
    }
  }
  (customer.to_string(), qty, cents)
}

fn merge(left : Array[(String, Int, Int)], right : Array[(String, Int, Int)]) -> Array[(String, Int, Int)] {
  let out = Array::new()
  let mut i = 0
  let mut j = 0
  while i < left.length() && j < right.length() {
    if left[i].0.lexical_compare(right[j].0) <= 0 {
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

fn merge_sort(rows : Array[(String, Int, Int)]) -> Array[(String, Int, Int)] {
  if rows.length() <= 1 {
    return rows
  }
  let mid = rows.length() / 2
  let left = Array::new()
  let right = Array::new()
  for i = 0; i < mid; i = i + 1 {
    left.push(rows[i])
  }
  for i = mid; i < rows.length(); i = i + 1 {
    right.push(rows[i])
  }
  merge(merge_sort(left), merge_sort(right))
}

fn aggregate(rows : Array[(String, Int, Int)]) -> Unit {
  let sorted = merge_sort(rows)
  let mut current = ""
  let mut count = 0
  let mut qty_sum = 0
  let mut cents_sum = 0
  for i = 0; i < sorted.length(); i = i + 1 {
    let row = sorted[i]
    if row.0 != current {
      if current.length() != 0 {
        println(current + "," + count.to_string() + "," + qty_sum.to_string() + "," + cents_sum.to_string())
      }
      current = row.0
      count = 0
      qty_sum = 0
      cents_sum = 0
    }
    count = count + 1
    qty_sum = qty_sum + row.1
    cents_sum = cents_sum + row.2
  }
  if current.length() != 0 {
    println(current + "," + count.to_string() + "," + qty_sum.to_string() + "," + cents_sum.to_string())
  }
}

fn process_line(line : String, rows : Array[(String, Int, Int)], seen_header : Bool) -> Bool {
  if line.length() == 0 {
    return seen_header
  }
  if !seen_header {
    return true
  }
  rows.push(parse_row(line))
  seen_header
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
  let rows = Array::new()
  let mut line = StringBuilder::new()
  let mut seen_header = false
  for _, ch in input {
    if ch == '\n' {
      seen_header = process_line(line.to_string(), rows, seen_header)
      line = StringBuilder::new()
    } else {
      line.write_char(ch)
    }
  }
  seen_header = process_line(line.to_string(), rows, seen_header)
  ignore(seen_header)
  aggregate(rows)
}
