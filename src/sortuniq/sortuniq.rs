use std::io::{self, BufRead, BufReader, Write};

fn main() {
    let stdin = io::stdin();
    let mut words: Vec<String> = Vec::with_capacity(1 << 18);
    for line in BufReader::new(stdin.lock()).lines() {
        let word = line.unwrap();
        if !word.is_empty() {
            words.push(word);
        }
    }

    words.sort_unstable();

    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    let mut i = 0usize;
    while i < words.len() {
        let word = &words[i];
        let mut count = 1usize;
        i += 1;
        while i < words.len() && words[i] == *word {
            count += 1;
            i += 1;
        }
        writeln!(out, "{word},{count}").unwrap();
    }
}
