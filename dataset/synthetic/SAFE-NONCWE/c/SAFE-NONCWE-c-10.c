#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node* create_node(int value) {
    Node *n = (Node *)malloc(sizeof(Node));
    if (!n) {
        return NULL;
    }
    n->value = value;
    n->next = NULL;
    return n;
}

Node* append(Node *head, int value) {
    Node *new_node = create_node(value);
    if (!new_node) {
        return head;
    }

    if (!head) {
        return new_node;
    }

    Node *curr = head;
    while (curr->next) {
        curr = curr->next;
    }

    curr->next = new_node;
    return head;
}

int sum_list(const Node *head) {
    int total = 0;
    const Node *curr = head;

    while (curr) {
        total += curr->value;
        curr = curr->next;
    }

    return total;
}

void free_list(Node *head) {
    Node *curr = head;

    while (curr) {
        Node *next = curr->next;
        free(curr);
        curr = next;
    }
}

int main(void) {
    Node *list = NULL;

    list = append(list, 4);
    list = append(list, 7);
    list = append(list, 1);
    list = append(list, 9);

    int total = sum_list(list);

    printf("Sum: %d\n", total);

    free_list(list);
    return 0;
}