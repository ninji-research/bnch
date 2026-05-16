fn is_prime(n : Int) -> Bool {
  if n < 2 {
    false
  } else if n % 2 == 0 {
    n == 2
  } else {
    let mut i = 3
    let mut ok = true
    while n / i >= i {
      if n % i == 0 {
        ok = false
      }
      i = i + 2
    }
    ok
  }
}

fn main {
  let n = if @env.args().length() > 1 {
    @strconv.parse_int(@env.args()[1]) catch {
      _ => 50000
    }
  } else {
    50000
  }
  let mut count = 0
  for i = 2; i <= n; i = i + 1 {
    if is_prime(i) {
      count = count + 1
    }
  }
  println(count.to_string())
}
