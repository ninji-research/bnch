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

fn fannkuch(n : Int) -> (Int, Int) {
  let p = Array::make(n, 0)
  let q = Array::make(n, 0)
  let s = Array::make(n, 0)
  for i = 0; i < n; i = i + 1 {
    p[i] = i
  }
  let mut max_flips = 0
  let mut sign = 1
  let mut checksum = 0
  let mut q0 = 0
  while true {
    q0 = p[0]
    if q0 != 0 {
      for i = 0; i < n; i = i + 1 {
        q[i] = p[i]
      }
      let mut flips = 1
      while true {
        let mut i = 1
        let mut j = q0 - 1
        while i < j {
          let t = q[i]
          q[i] = q[j]
          q[j] = t
          i = i + 1
          j = j - 1
        }
        let t = q[q0]
        q[q0] = q0
        q0 = t
        if q0 == 0 {
          break
        }
        flips = flips + 1
      }
      if flips > max_flips {
        max_flips = flips
      }
      checksum = checksum + sign * flips
    }
    if sign == 1 {
      let t = p[1]
      p[1] = p[0]
      p[0] = t
      sign = -1
    } else {
      let t = p[1]
      p[1] = p[2]
      p[2] = t
      sign = 1
      let mut i = 2
      while true {
        let sx = s[i]
        if sx < i {
          s[i] = sx + 1
          break
        }
        s[i] = 0
        let mut j = 0
        let t = p[0]
        while j < i {
          p[j] = p[j + 1]
          j = j + 1
        }
        p[i] = t
        i = i + 1
        if i == n {
          return (checksum, max_flips)
        }
      }
    }
  }
  (checksum, max_flips)
}

fn main {
  let n = arg_or(1, 10)
  let result = fannkuch(n)
  println(result.0.to_string())
  println("Pfannkuchen(" + n.to_string() + ") = " + result.1.to_string())
}
