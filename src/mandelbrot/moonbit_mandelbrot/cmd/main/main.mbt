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

fn main {
  let size = arg_or(1, 4000)
  let mut sum = 0
  for y = 0; y < size; y = y + 1 {
    for x = 0; x < size / 8; x = x + 1 {
      let mut byte_val = 0
      for b = 0; b < 8; b = b + 1 {
        let ci = y.to_double() * 2.0 / size.to_double() - 1.0
        let cr = (x * 8 + b).to_double() * 2.0 / size.to_double() - 1.5
        let mut zr = 0.0
        let mut zi = 0.0
        let mut tr = 0.0
        let mut ti = 0.0
        let mut i = 0
        while i < 50 && tr + ti <= 4.0 {
          zi = 2.0 * zr * zi + ci
          zr = tr - ti + cr
          tr = zr * zr
          ti = zi * zi
          i = i + 1
        }
        if tr + ti <= 4.0 {
          byte_val = byte_val.lor(1 << (7 - b))
        }
      }
      sum = sum + byte_val
    }
  }
  println(sum.to_string())
}
