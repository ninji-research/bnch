use std::io::{self, Write};

const WIDTH: usize = 60;
const IM: u32 = 139_968;
const IA: u32 = 3_877;
const IC: u32 = 29_573;

#[derive(Clone, Copy)]
struct AminoAcid {
    ch: u8,
    p: f64,
}

const ALU: &str = concat!(
    "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG",
    "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA",
    "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT",
    "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA",
    "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG",
    "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC",
    "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA",
);

const IUB: [AminoAcid; 15] = [
    AminoAcid { ch: b'a', p: 0.27 },
    AminoAcid { ch: b'c', p: 0.12 },
    AminoAcid { ch: b'g', p: 0.12 },
    AminoAcid { ch: b't', p: 0.27 },
    AminoAcid { ch: b'B', p: 0.02 },
    AminoAcid { ch: b'D', p: 0.02 },
    AminoAcid { ch: b'H', p: 0.02 },
    AminoAcid { ch: b'K', p: 0.02 },
    AminoAcid { ch: b'M', p: 0.02 },
    AminoAcid { ch: b'N', p: 0.02 },
    AminoAcid { ch: b'R', p: 0.02 },
    AminoAcid { ch: b'S', p: 0.02 },
    AminoAcid { ch: b'V', p: 0.02 },
    AminoAcid { ch: b'W', p: 0.02 },
    AminoAcid { ch: b'Y', p: 0.02 },
];

const HOMO_SAPIENS: [AminoAcid; 4] = [
    AminoAcid {
        ch: b'a',
        p: 0.3029549426680,
    },
    AminoAcid {
        ch: b'c',
        p: 0.1979883004921,
    },
    AminoAcid {
        ch: b'g',
        p: 0.1975473066391,
    },
    AminoAcid {
        ch: b't',
        p: 0.3015094502008,
    },
];

struct Random(u32);

impl Random {
    fn next(&mut self) -> f64 {
        self.0 = (self.0 * IA + IC) % IM;
        self.0 as f64 / IM as f64
    }
}

fn cumulative(table: &[AminoAcid]) -> Vec<AminoAcid> {
    let mut total = 0.0;
    table.iter()
        .map(|item| {
            total += item.p;
            AminoAcid {
                ch: item.ch,
                p: total,
            }
        })
        .collect()
}

fn write_repeat(out: &mut Vec<u8>, header: &str, sequence: &[u8], mut length: usize) {
    out.extend_from_slice(header.as_bytes());
    out.push(b'\n');
    let mut offset = 0usize;
    while length > 0 {
        let line_len = length.min(WIDTH);
        for i in 0..line_len {
            out.push(sequence[(offset + i) % sequence.len()]);
        }
        out.push(b'\n');
        offset = (offset + line_len) % sequence.len();
        length -= line_len;
    }
}

fn pick(table: &[AminoAcid], rng: &mut Random) -> u8 {
    let value = rng.next();
    for item in table {
        if value < item.p {
            return item.ch;
        }
    }
    table[table.len() - 1].ch
}

fn write_random(out: &mut Vec<u8>, header: &str, table: &[AminoAcid], rng: &mut Random, mut length: usize) {
    out.extend_from_slice(header.as_bytes());
    out.push(b'\n');
    while length > 0 {
        let line_len = length.min(WIDTH);
        for _ in 0..line_len {
            out.push(pick(table, rng));
        }
        out.push(b'\n');
        length -= line_len;
    }
}

fn main() {
    let n = std::env::args()
        .nth(1)
        .and_then(|value| value.parse::<usize>().ok())
        .unwrap_or(250_000);

    let iub = cumulative(&IUB);
    let homo = cumulative(&HOMO_SAPIENS);
    let mut rng = Random(42);
    let mut out = Vec::with_capacity(n * 11);

    write_repeat(&mut out, ">ONE Homo sapiens alu", ALU.as_bytes(), n * 2);
    write_random(&mut out, ">TWO IUB ambiguity codes", &iub, &mut rng, n * 3);
    write_random(&mut out, ">THREE Homo sapiens frequency", &homo, &mut rng, n * 5);

    io::stdout().write_all(&out).unwrap();
}
