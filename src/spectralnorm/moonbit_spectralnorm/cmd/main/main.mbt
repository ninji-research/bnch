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

fn eval_A(i : Int, j : Int) -> Double {
  1.0 / ((i + j) * (i + j + 1) / 2 + i + 1).to_double()
}

fn eval_A_times_u(u : Array[Double], au : Array[Double]) -> Unit {
  let n = u.length()
  for i = 0; i < n; i = i + 1 {
    au[i] = 0.0
    for j = 0; j < n; j = j + 1 {
      au[i] = au[i] + eval_A(i, j) * u[j]
    }
  }
}

fn eval_At_times_u(u : Array[Double], au : Array[Double]) -> Unit {
  let n = u.length()
  for i = 0; i < n; i = i + 1 {
    au[i] = 0.0
    for j = 0; j < n; j = j + 1 {
      au[i] = au[i] + eval_A(j, i) * u[j]
    }
  }
}

fn eval_AtA_times_u(u : Array[Double], v : Array[Double], w : Array[Double]) -> Unit {
  eval_A_times_u(u, w)
  eval_At_times_u(w, v)
}

fn main {
  let n = arg_or(1, 5500)
  let u = Array::make(n, 1.0)
  let v = Array::make(n, 0.0)
  let w = Array::make(n, 0.0)
  for i = 0; i < 10; i = i + 1 {
    eval_AtA_times_u(u, v, w)
    eval_AtA_times_u(v, u, w)
  }
  let mut vBv = 0.0
  let mut vv = 0.0
  for i = 0; i < n; i = i + 1 {
    vBv = vBv + u[i] * v[i]
    vv = vv + v[i] * v[i]
  }
  
  let result = (vBv / vv).sqrt()
  println(result.to_string())
}
