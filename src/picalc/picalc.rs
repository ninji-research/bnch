use std::thread;

fn xorshift32(state: &mut u32) -> f64 {
    let mut x = *state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *state = x;
    (x as f64) / 4294967295.0
}

fn worker(start_seed: u32, iterations: usize) -> usize {
    let mut state = start_seed;
    let mut inside = 0;
    for _ in 0..iterations {
        let x = xorshift32(&mut state);
        let y = xorshift32(&mut state);
        if x * x + y * y <= 1.0 {
            inside += 1;
        }
    }
    inside
}

fn main() {
    let total_iters = std::env::args().nth(1).and_then(|x| x.parse().ok()).unwrap_or(50_000_000usize);
    let threads = std::env::args()
        .nth(2)
        .and_then(|x| x.parse().ok())
        .filter(|&count: &usize| count > 0)
        .unwrap_or(4);

    let mut handles = vec![];
    for i in 0..threads {
        let start = (total_iters * i) / threads;
        let end = (total_iters * (i + 1)) / threads;
        let iterations = end - start;
        handles.push(thread::spawn(move || {
            worker(12345 + i as u32, iterations)
        }));
    }
    
    let mut total_inside = 0;
    for handle in handles {
        total_inside += handle.join().unwrap();
    }
    
    let pi = 4.0 * (total_inside as f64) / (total_iters as f64);
    println!("{:.5}", pi);
}
