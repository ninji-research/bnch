fn fannkuch(n: usize) -> (i32, i32) {
    let mut p = (0..n).collect::<Vec<_>>();
    let mut q = vec![0; n];
    let mut s = vec![0; n];
    let mut sign = 1;
    let mut max_flips = 0;
    let mut sum = 0;
    loop {
        let mut q0 = p[0];
        if q0 != 0 {
            for i in 1..n { q[i] = p[i]; }
            let mut flips = 1;
            loop {
                let mut i = 1;
                let mut j = q0 - 1;
                while i < j {
                    q.swap(i, j);
                    i += 1;
                    j -= 1;
                }
                let t = q[q0];
                q[q0] = q0 as usize;
                q0 = t;
                if q0 == 0 { break; }
                flips += 1;
            }
            if flips > max_flips { max_flips = flips; }
            sum += sign * flips;
        }
        if sign == 1 {
            p.swap(0, 1);
            sign = -1;
        } else {
            p.swap(1, 2);
            sign = 1;
            for i in 2..n {
                let sx = s[i];
                if sx < i {
                    s[i] = sx + 1;
                    break;
                }
                s[i] = 0;
                let t = p[0];
                for j in 0..i { p[j] = p[j+1]; }
                p[i] = t;
                if i == n - 1 { return (sum, max_flips); }
            }
        }
    }
}

fn main() {
    let n = std::env::args().nth(1).and_then(|x| x.parse().ok()).unwrap_or(11);
    let (sum, max_flips) = fannkuch(n);
    println!("{}\nPfannkuchen({}) = {}", sum, n, max_flips);
}
