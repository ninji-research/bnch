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

fn xorshift32(state : Ref[UInt]) -> Double {
  let mut x = state.val
  x = x.lxor(x << 13)
  x = x.lxor(x >> 17)
  x = x.lxor(x << 5)
  state.val = x
  x.to_double() / 4294967295.0
}

fn worker(start_seed : UInt, iterations : Int) -> Int {
  let state = @ref.new(start_seed)
  let mut inside = 0
  for i = 0; i < iterations; i = i + 1 {
    let x = xorshift32(state)
    let y = xorshift32(state)
    if x * x + y * y <= 1.0 {
      inside = inside + 1
    }
  }
  inside
}

fn main {
  let total_iters = arg_or(1, 50_000_000)
  let num_threads = if arg_or(2, 1) > 0 { arg_or(2, 1) } else { 1 }
  let mut total_inside = 0
  
  for i = 0; i < num_threads; i = i + 1 {
    let start = (total_iters * i) / num_threads
    let finish = (total_iters * (i + 1)) / num_threads
    total_inside = total_inside + worker(12345U + i.reinterpret_as_uint(), finish - start)
  }
  
  let pi = 4.0 * total_inside.to_double() / total_iters.to_double()
  println(pi.to_string())
}
