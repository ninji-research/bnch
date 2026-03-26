fn string_char_at(text : String, index : Int) -> Char {
  text[index].to_int().unsafe_to_char()
}

fn split4(line : String) -> (String, String, String, String) {
  let first = StringBuilder::new()
  let second = StringBuilder::new()
  let third = StringBuilder::new()
  let fourth = StringBuilder::new()
  let mut field = 0
  for _, ch in line {
    if ch == ',' {
      field = field + 1
    } else if field == 0 {
      first.write_char(ch)
    } else if field == 1 {
      second.write_char(ch)
    } else if field == 2 {
      third.write_char(ch)
    } else {
      fourth.write_char(ch)
    }
  }
  (first.to_string(), second.to_string(), third.to_string(), fourth.to_string())
}

fn merge_users(left : Array[(String, String, String)], right : Array[(String, String, String)]) -> Array[(String, String, String)] {
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

fn merge_events(left : Array[(String, Int, Int)], right : Array[(String, Int, Int)]) -> Array[(String, Int, Int)] {
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

fn merge_joined(left : Array[(String, String, Int, Int)], right : Array[(String, String, Int, Int)]) -> Array[(String, String, Int, Int)] {
  let out = Array::new()
  let mut i = 0
  let mut j = 0
  while i < left.length() && j < right.length() {
    let cmp = left[i].0.lexical_compare(right[j].0)
    if cmp < 0 || (cmp == 0 && left[i].1.lexical_compare(right[j].1) <= 0) {
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

fn sort_users(rows : Array[(String, String, String)]) -> Array[(String, String, String)] {
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
  merge_users(sort_users(left), sort_users(right))
}

fn sort_events(rows : Array[(String, Int, Int)]) -> Array[(String, Int, Int)] {
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
  merge_events(sort_events(left), sort_events(right))
}

fn sort_joined(rows : Array[(String, String, Int, Int)]) -> Array[(String, String, Int, Int)] {
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
  merge_joined(sort_joined(left), sort_joined(right))
}

fn process_line(
  line : String,
  section : String,
  users : Array[(String, String, String)],
  events : Array[(String, Int, Int)],
) -> Unit {
  if line.length() == 0 || line == "user_id,region,tier,status" || line == "user_id,kind,latency_ms,bytes" {
    return
  }
  if section == "[users]" {
    let row = split4(line)
    if row.3 == "active" {
      users.push((row.0, row.1, row.2))
    }
  } else if section == "[events]" {
    let row = split4(line)
    if row.1 != "noop" {
      let latency = @strconv.parse_int(row.2) catch { _ => 0 }
      let bytes = @strconv.parse_int(row.3) catch { _ => 0 }
      events.push((row.0, latency, bytes))
    }
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
  let users = Array::new()
  let events = Array::new()
  let mut line = StringBuilder::new()
  let mut section = ""

  fn flush_line(
    text : String,
    section_ref : String,
    users : Array[(String, String, String)],
    events : Array[(String, Int, Int)],
  ) -> String {
    if text == "[users]" || text == "[events]" {
      return text
    }
    process_line(text, section_ref, users, events)
    section_ref
  }

  for _, ch in input {
    if ch == '\n' {
      section = flush_line(line.to_string(), section, users, events)
      line = StringBuilder::new()
    } else {
      line.write_char(ch)
    }
  }
  section = flush_line(line.to_string(), section, users, events)
  ignore(section)

  let sorted_users = sort_users(users)
  let sorted_events = sort_events(events)
  let joined = Array::new()
  let mut i = 0
  let mut j = 0
  while i < sorted_users.length() && j < sorted_events.length() {
    let user = sorted_users[i]
    let event = sorted_events[j]
    let cmp = user.0.lexical_compare(event.0)
    if cmp < 0 {
      i = i + 1
    } else if cmp > 0 {
      j = j + 1
    } else {
      while j < sorted_events.length() && sorted_events[j].0 == user.0 {
        let current = sorted_events[j]
        joined.push((user.1, user.2, current.1, current.2))
        j = j + 1
      }
      i = i + 1
    }
  }

  let sorted_joined = sort_joined(joined)
  let mut current_region = ""
  let mut current_tier = ""
  let mut count = 0
  let mut latency_sum = 0
  let mut bytes_sum = 0
  for i = 0; i < sorted_joined.length(); i = i + 1 {
    let row = sorted_joined[i]
    if row.0 != current_region || row.1 != current_tier {
      if current_region.length() != 0 {
        println(current_region + "," + current_tier + "," + count.to_string() + "," + latency_sum.to_string() + "," + bytes_sum.to_string())
      }
      current_region = row.0
      current_tier = row.1
      count = 0
      latency_sum = 0
      bytes_sum = 0
    }
    count = count + 1
    latency_sum = latency_sum + row.2
    bytes_sum = bytes_sum + row.3
  }
  if current_region.length() != 0 {
    println(current_region + "," + current_tier + "," + count.to_string() + "," + latency_sum.to_string() + "," + bytes_sum.to_string())
  }
}
