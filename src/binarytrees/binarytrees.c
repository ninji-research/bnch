#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    struct Node *left;
    struct Node *right;
} Node;

static Node *bottom_up_tree(int depth) {
    Node *node = (Node *)malloc(sizeof(Node));
    if (node == NULL) {
        perror("malloc");
        exit(1);
    }
    if (depth > 0) {
        node->left = bottom_up_tree(depth - 1);
        node->right = bottom_up_tree(depth - 1);
    } else {
        node->left = NULL;
        node->right = NULL;
    }
    return node;
}

static uint32_t item_check(const Node *node) {
    if (node->left == NULL) {
        return 1;
    }
    return 1 + item_check(node->left) + item_check(node->right);
}

static void free_tree(Node *node) {
    if (node->left != NULL) {
        free_tree(node->left);
        free_tree(node->right);
    }
    free(node);
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 21;
    int min_depth = 4;
    int max_depth = min_depth + 2 > n ? min_depth + 2 : n;
    int stretch_depth = max_depth + 1;

    Node *stretch_tree = bottom_up_tree(stretch_depth);
    printf(
        "stretch tree of depth %d\t check: %u\n",
        stretch_depth,
        item_check(stretch_tree)
    );
    free_tree(stretch_tree);

    Node *long_lived_tree = bottom_up_tree(max_depth);

    for (int depth = min_depth; depth <= max_depth; depth += 2) {
        int iterations = 1 << (max_depth - depth + min_depth);
        uint32_t check = 0;
        for (int i = 0; i < iterations; ++i) {
            Node *tree = bottom_up_tree(depth);
            check += item_check(tree);
            free_tree(tree);
        }
        printf("%d\t trees of depth %d\t check: %u\n", iterations, depth, check);
    }

    printf(
        "long lived tree of depth %d\t check: %u\n",
        max_depth,
        item_check(long_lived_tree)
    );
    free_tree(long_lived_tree);
    return 0;
}
