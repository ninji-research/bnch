use std::io::{self, BufRead, BufReader, Write};

#[derive(Clone)]
struct User {
    id: String,
    region: String,
    tier: String,
}

#[derive(Clone)]
struct Event {
    id: String,
    latency_ms: i64,
    bytes: i64,
}

#[derive(Clone)]
struct Joined {
    region: String,
    tier: String,
    latency_ms: i64,
    bytes: i64,
}

fn parse_user(line: &str) -> Option<User> {
    let mut parts = line.splitn(4, ',');
    let id = parts.next()?;
    let region = parts.next()?;
    let tier = parts.next()?;
    let status = parts.next()?;
    if status != "active" {
        return None;
    }
    Some(User {
        id: id.to_owned(),
        region: region.to_owned(),
        tier: tier.to_owned(),
    })
}

fn parse_event(line: &str) -> Option<Event> {
    let mut parts = line.splitn(4, ',');
    let id = parts.next()?;
    let kind = parts.next()?;
    let latency_ms = parts.next()?.parse::<i64>().ok()?;
    let bytes = parts.next()?.parse::<i64>().ok()?;
    if kind == "noop" {
        return None;
    }
    Some(Event {
        id: id.to_owned(),
        latency_ms,
        bytes,
    })
}

fn main() {
    let stdin = io::stdin();
    let reader = BufReader::new(stdin.lock());
    let mut users: Vec<User> = Vec::with_capacity(1 << 15);
    let mut events: Vec<Event> = Vec::with_capacity(1 << 18);
    let mut in_users = false;
    let mut in_events = false;
    let mut header_pending = false;

    for line in reader.lines() {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        if line == "[users]" || line == "[events]" {
            in_users = line == "[users]";
            in_events = line == "[events]";
            header_pending = true;
            continue;
        }
        if header_pending {
            header_pending = false;
            continue;
        }
        if in_users {
            if let Some(user) = parse_user(&line) {
                users.push(user);
            }
        } else if in_events {
            if let Some(event) = parse_event(&line) {
                events.push(event);
            }
        }
    }

    users.sort_unstable_by(|a, b| a.id.cmp(&b.id));
    events.sort_unstable_by(|a, b| a.id.cmp(&b.id));

    let mut joined: Vec<Joined> = Vec::with_capacity(events.len());
    let mut user_index = 0usize;
    let mut event_index = 0usize;
    while user_index < users.len() && event_index < events.len() {
        match users[user_index].id.cmp(&events[event_index].id) {
            std::cmp::Ordering::Less => user_index += 1,
            std::cmp::Ordering::Greater => event_index += 1,
            std::cmp::Ordering::Equal => {
                let user = &users[user_index];
                while event_index < events.len() && events[event_index].id == user.id {
                    joined.push(Joined {
                        region: user.region.clone(),
                        tier: user.tier.clone(),
                        latency_ms: events[event_index].latency_ms,
                        bytes: events[event_index].bytes,
                    });
                    event_index += 1;
                }
                user_index += 1;
            }
        }
    }

    joined.sort_unstable_by(|a, b| {
        a.region
            .cmp(&b.region)
            .then_with(|| a.tier.cmp(&b.tier))
    });

    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    let mut i = 0usize;
    while i < joined.len() {
        let region = joined[i].region.clone();
        let tier = joined[i].tier.clone();
        let mut count = 0i64;
        let mut latency_sum = 0i64;
        let mut bytes_sum = 0i64;
        while i < joined.len() && joined[i].region == region && joined[i].tier == tier {
            count += 1;
            latency_sum += joined[i].latency_ms;
            bytes_sum += joined[i].bytes;
            i += 1;
        }
        writeln!(out, "{region},{tier},{count},{latency_sum},{bytes_sum}").unwrap();
    }
}
