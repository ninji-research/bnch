use std::cmp::Ordering;
use std::io::{self, Read};

const TARGETS: [&str; 5] = [
    "GGT",
    "GGTA",
    "GGTATT",
    "GGTATTTTAATT",
    "GGTATTTTAATTTATAGT",
];

fn encode_base(ch: u8) -> usize {
    match ch {
        b'A' => 0,
        b'C' => 1,
        b'G' => 2,
        b'T' => 3,
        _ => usize::MAX,
    }
}

fn decode_base(code: usize) -> u8 {
    b"ACGT"[code & 3]
}

fn read_three_sequence() -> Vec<u8> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut in_three = false;
    let mut sequence = Vec::new();
    for line in input.lines() {
        if let Some(header) = line.strip_prefix('>') {
            if in_three {
                break;
            }
            in_three = header.starts_with("THREE");
            continue;
        }
        if !in_three {
            continue;
        }
        for mut byte in line.bytes() {
            byte.make_ascii_uppercase();
            if encode_base(byte) != usize::MAX {
                sequence.push(byte);
            }
        }
    }
    sequence
}

fn print_frequencies(sequence: &[u8], k: usize) {
    if sequence.len() < k {
        println!();
        return;
    }
    let bucket_count = 1usize << (2 * k);
    let mask = bucket_count - 1;
    let mut counts = vec![0usize; bucket_count];
    let mut rolling = 0usize;
    for &byte in sequence.iter().take(k) {
        rolling = (rolling << 2) | encode_base(byte);
    }
    counts[rolling] += 1;
    for &byte in sequence.iter().skip(k) {
        rolling = ((rolling << 2) & mask) | encode_base(byte);
        counts[rolling] += 1;
    }

    let mut entries: Vec<(Vec<u8>, usize)> = counts
        .into_iter()
        .enumerate()
        .filter(|(_, count)| *count > 0)
        .map(|(code, count)| {
            let mut key = vec![b'A'; k];
            let mut value = code;
            for index in (0..k).rev() {
                key[index] = decode_base(value);
                value >>= 2;
            }
            (key, count)
        })
        .collect();

    entries.sort_by(|a, b| match b.1.cmp(&a.1) {
        Ordering::Equal => a.0.cmp(&b.0),
        other => other,
    });

    let total = (sequence.len() - k + 1) as f64;
    for (key, count) in entries {
        println!(
            "{} {:.3}",
            String::from_utf8(key).unwrap(),
            100.0 * count as f64 / total
        );
    }
    println!();
}

fn count_fragment(sequence: &[u8], fragment: &[u8]) -> usize {
    if sequence.len() < fragment.len() {
        return 0;
    }
    sequence
        .windows(fragment.len())
        .filter(|window| *window == fragment)
        .count()
}

fn main() {
    let sequence = read_three_sequence();
    print_frequencies(&sequence, 1);
    print_frequencies(&sequence, 2);
    for target in TARGETS {
        println!("{}\t{}", count_fragment(&sequence, target.as_bytes()), target);
    }
}
