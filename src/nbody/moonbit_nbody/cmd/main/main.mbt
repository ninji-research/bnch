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

struct Body {
  mut x : Double
  mut y : Double
  mut z : Double
  mut vx : Double
  mut vy : Double
  mut vz : Double
  mass : Double
}

let solar_mass : Double = 4.0 * 3.14159265358979323846 * 3.14159265358979323846
let days_per_year : Double = 365.24

fn make_body(x : Double, y : Double, z : Double, vx : Double, vy : Double, vz : Double, mass : Double) -> Body {
  { x, y, z, vx: vx * days_per_year, vy: vy * days_per_year, vz: vz * days_per_year, mass: mass * solar_mass }
}

let bodies : Array[Body] = [
  { x: 0.0, y: 0.0, z: 0.0, vx: 0.0, vy: 0.0, vz: 0.0, mass: solar_mass },
  make_body(4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01, 1.66007664274403694e-03, 7.69901118419740425e-03, -6.90460016972063023e-05, 9.54791938424326609e-04),
  make_body(8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01, -2.76742510726862411e-03, 4.99852801234917238e-03, 2.30417297573763929e-05, 2.85885980666130812e-04),
  make_body(1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01, 2.96460137564761618e-03, 2.37847173959480950e-03, -2.96589568540237556e-05, 4.36624404335156298e-05),
  make_body(1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01, 2.68067772490389322e-03, 1.62824170038242295e-03, -9.51592254519715870e-05, 5.15138902046611451e-05)
]

fn advance(bodies : Array[Body], dt : Double) -> Unit {
  let n = bodies.length()
  for i = 0; i < n; i = i + 1 {
    let b = bodies[i]
    for j = i + 1; j < n; j = j + 1 {
      let b_prime = bodies[j]
      let dx = b.x - b_prime.x
      let dy = b.y - b_prime.y
      let dz = b.z - b_prime.z
      let d2 = dx * dx + dy * dy + dz * dz
      let mag = dt / (d2 * d2.sqrt())
      b.vx = b.vx - dx * b_prime.mass * mag
      b.vy = b.vy - dy * b_prime.mass * mag
      b.vz = b.vz - dz * b_prime.mass * mag
      b_prime.vx = b_prime.vx + dx * b.mass * mag
      b_prime.vy = b_prime.vy + dy * b.mass * mag
      b_prime.vz = b_prime.vz + dz * b.mass * mag
    }
  }
  for i = 0; i < n; i = i + 1 {
    let b = bodies[i]
    b.x = b.x + dt * b.vx
    b.y = b.y + dt * b.vy
    b.z = b.z + dt * b.vz
  }
}

fn energy(bodies : Array[Body]) -> Double {
  let mut e = 0.0
  let n = bodies.length()
  for i = 0; i < n; i = i + 1 {
    let b = bodies[i]
    e = e + 0.5 * b.mass * (b.vx * b.vx + b.vy * b.vy + b.vz * b.vz)
    for j = i + 1; j < n; j = j + 1 {
      let b_prime = bodies[j]
      let dx = b.x - b_prime.x
      let dy = b.y - b_prime.y
      let dz = b.z - b_prime.z
      e = e - (b.mass * b_prime.mass) / (dx * dx + dy * dy + dz * dz).sqrt()
    }
  }
  e
}

fn offset_momentum(bodies : Array[Body]) -> Unit {
  let mut px = 0.0
  let mut py = 0.0
  let mut pz = 0.0
  for i = 0; i < bodies.length(); i = i + 1 {
    let b = bodies[i]
    px = px + b.vx * b.mass
    py = py + b.vy * b.mass
    pz = pz + b.vz * b.mass
  }
  bodies[0].vx = -px / solar_mass
  bodies[0].vy = -py / solar_mass
  bodies[0].vz = -pz / solar_mass
}

fn main {
  let n = arg_or(1, 10000000)
  offset_momentum(bodies)
  println(energy(bodies).to_string())
  for i = 1; i <= n; i = i + 1 {
    advance(bodies, 0.01)
  }
  println(energy(bodies).to_string())
}
