fn is_prime(n: i32) -> bool {
    if n < 2 {
        return false;
    }
    if n % 2 == 0 {
        return n == 2;
    }
    let mut i = 3;
    while n / i >= i {
        if n % i == 0 {
            return false;
        }
        i += 2;
    }
    true
}

fn main() {
    let n = std::env::args()
        .nth(1)
        .and_then(|x| x.parse().ok())
        .unwrap_or(50000);
    let mut count = 0;
    for i in 2..=n {
        if is_prime(i) {
            count += 1;
        }
    }
    println!("{count}");
}
