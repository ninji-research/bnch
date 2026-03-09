fn ackermann(m: u32, n: u32) -> u32 {
    if m == 0 {
        n + 1
    } else if m > 0 && n == 0 {
        ackermann(m - 1, 1)
    } else {
        ackermann(m - 1, ackermann(m, n - 1))
    }
}
fn main() {
    let mut args = std::env::args();
    args.next();
    let m = args.next().and_then(|x| x.parse().ok()).unwrap_or(3);
    let n = args.next().and_then(|x| x.parse().ok()).unwrap_or(11);
    println!("{}", ackermann(m, n));
}
