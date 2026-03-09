enum Node {
    Leaf,
    Branch(Box<Node>, Box<Node>),
}

fn item_check(node: &Node) -> u32 {
    match node {
        Node::Leaf => 1,
        Node::Branch(left, right) => 1 + item_check(left) + item_check(right),
    }
}

fn bottom_up_tree(depth: u32) -> Node {
    if depth > 0 {
        Node::Branch(
            Box::new(bottom_up_tree(depth - 1)),
            Box::new(bottom_up_tree(depth - 1)),
        )
    } else {
        Node::Leaf
    }
}

fn main() {
    let n = std::env::args()
        .nth(1)
        .and_then(|x| x.parse().ok())
        .unwrap_or(21);
    let min_depth = 4;
    let max_depth = if min_depth + 2 > n { min_depth + 2 } else { n };
    let stretch_depth = max_depth + 1;

    let stretch_tree = bottom_up_tree(stretch_depth);
    println!(
        "stretch tree of depth {}\t check: {}",
        stretch_depth,
        item_check(&stretch_tree)
    );

    let long_lived_tree = bottom_up_tree(max_depth);

    let mut depth = min_depth;
    while depth <= max_depth {
        let iterations = 1 << (max_depth - depth + min_depth);
        let mut check = 0;

        for _ in 1..=iterations {
            let tree = bottom_up_tree(depth);
            check += item_check(&tree);
        }
        println!("{}\t trees of depth {}\t check: {}", iterations, depth, check);
        depth += 2;
    }

    println!(
        "long lived tree of depth {}\t check: {}",
        max_depth,
        item_check(&long_lived_tree)
    );
}
