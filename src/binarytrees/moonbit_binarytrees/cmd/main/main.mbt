fn arg_or(index : Int, fallback : Int) -> Int {
  let args = @env.args()
  if args.length() > index {
    @strconv.parse_int(args[index]) catch {
      _ => fallback
    }
  } else {
    fallback
  }
}

enum Node {
  Leaf
  Node(Node, Node)
}

fn item_check(node : Node) -> Int {
  match node {
    Leaf => 1
    Node(l, r) => 1 + item_check(l) + item_check(r)
  }
}

fn bottom_up_tree(depth : Int) -> Node {
  if depth > 0 {
    Node(bottom_up_tree(depth - 1), bottom_up_tree(depth - 1))
  } else {
    Leaf
  }
}

fn main {
  let n = arg_or(1, 21)
  let min_depth = 4
  let max_depth = if min_depth + 2 > n { min_depth + 2 } else { n }
  let stretch_depth = max_depth + 1
  let stretch_tree = bottom_up_tree(stretch_depth)
  println("stretch tree of depth " + stretch_depth.to_string() + "\t check: " + item_check(stretch_tree).to_string())
  let long_lived_tree = bottom_up_tree(max_depth)
  
  let mut depth = min_depth
  while depth <= max_depth {
    let iterations = 1 << (max_depth - depth + min_depth)
    let mut check = 0
    for i = 1; i <= iterations; i = i + 1 {
      check = check + item_check(bottom_up_tree(depth))
    }
    println(iterations.to_string() + "\t trees of depth " + depth.to_string() + "\t check: " + check.to_string())
    depth = depth + 2
  }
  println("long lived tree of depth " + max_depth.to_string() + "\t check: " + item_check(long_lived_tree).to_string())
}
