use std::io::{self, Read, Write};

const WIDTH: usize = 60;

fn complement_table() -> [u8; 256] {
    let mut table = [0u8; 256];
    for (index, slot) in table.iter_mut().enumerate() {
        *slot = index as u8;
    }
    for (&from, &to) in b"ACBDGHKMNSRUTWVYacbdghkmnsrutwvy"
        .iter()
        .zip(b"TGVHCDMKNSYAAWBRTgvhcdmknsyaawbr".iter())
    {
        table[from as usize] = to;
    }
    table
}

fn emit_record(out: &mut Vec<u8>, table: &[u8; 256], header: &[u8], sequence: &[u8]) {
    if header.is_empty() {
        return;
    }
    out.extend_from_slice(header);
    out.push(b'\n');
    let mut line_len = 0usize;
    for &byte in sequence.iter().rev() {
        out.push(table[byte as usize]);
        line_len += 1;
        if line_len == WIDTH {
            out.push(b'\n');
            line_len = 0;
        }
    }
    if line_len != 0 {
        out.push(b'\n');
    }
}

fn main() {
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).unwrap();

    let table = complement_table();
    let mut out = Vec::with_capacity(input.len() + input.len() / WIDTH + 32);
    let mut header = Vec::new();
    let mut sequence = Vec::new();

    for raw_line in input.split(|&byte| byte == b'\n') {
        let line = if raw_line.ends_with(b"\r") {
            &raw_line[..raw_line.len() - 1]
        } else {
            raw_line
        };
        if line.first() == Some(&b'>') {
            emit_record(&mut out, &table, &header, &sequence);
            header.clear();
            header.extend_from_slice(line);
            sequence.clear();
            continue;
        }
        for &byte in line {
            if !byte.is_ascii_whitespace() {
                sequence.push(byte);
            }
        }
    }

    emit_record(&mut out, &table, &header, &sequence);
    io::stdout().write_all(&out).unwrap();
}
