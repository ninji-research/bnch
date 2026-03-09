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

fn ackermann(m : Int, n : Int) -> Int {
  if m == 0 {
    n + 1
  } else if m > 0 && n == 0 {
    ackermann(m - 1, 1)
  } else {
    ackermann(m - 1, ackermann(m, n - 1))
  }
}
fn main {
  let m = arg_or(1, 3)
  let n = arg_or(2, 11)
  println(ackermann(m, n).to_string())
}
