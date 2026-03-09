fn main() {
    let size = std::env::args().nth(1).and_then(|x| x.parse().ok()).unwrap_or(4000);
    let inv_size = 2.0 / (size as f64);
    let mut sum: u32 = 0;
    for y in 0..size {
        let ci = (y as f64) * inv_size - 1.0;
        for x in 0..size / 8 {
            let mut byte = 0;
            for b in 0..8 {
                let cr = ((x * 8 + b) as f64) * inv_size - 1.5;
                let mut zr = 0.0;
                let mut zi = 0.0;
                let mut tr = 0.0;
                let mut ti = 0.0;
                let mut i = 0;
                while i < 50 && tr + ti <= 4.0 {
                    zi = 2.0 * zr * zi + ci;
                    zr = tr - ti + cr;
                    tr = zr * zr;
                    ti = zi * zi;
                    i += 1;
                }
                if tr + ti <= 4.0 {
                    byte |= 1 << (7 - b);
                }
            }
            sum += byte as u32;
        }
    }
    println!("{}", sum);
}
