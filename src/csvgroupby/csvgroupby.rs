use std::collections::BTreeMap;
use std::io::{self, BufRead, BufReader, Write};

#[derive(Clone, Copy, Default)]
struct Stats {
    count: i64,
    qty: i64,
    cents: i64,
}

fn main() {
    let stdin = io::stdin();
    let mut reader = BufReader::new(stdin.lock());
    let mut line = String::new();
    if reader.read_line(&mut line).unwrap() == 0 {
        return;
    }

    let mut aggregates: BTreeMap<String, Stats> = BTreeMap::new();
    line.clear();
    while reader.read_line(&mut line).unwrap() > 0 {
        let trimmed = line.trim_end_matches(['\n', '\r']);
        let mut parts = trimmed.splitn(4, ',');
        let customer = parts.next().unwrap();
        let _sku = parts.next().unwrap();
        let qty = parts.next().unwrap().parse::<i64>().unwrap();
        let cents = parts.next().unwrap().parse::<i64>().unwrap();

        let entry = aggregates.entry(customer.to_owned()).or_default();
        entry.count += 1;
        entry.qty += qty;
        entry.cents += cents;
        line.clear();
    }

    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    for (customer, stats) in aggregates {
        writeln!(
            out,
            "{},{},{},{}",
            customer, stats.count, stats.qty, stats.cents
        )
        .unwrap();
    }
}
