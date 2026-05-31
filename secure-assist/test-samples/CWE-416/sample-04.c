#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node *head = NULL;

void push(int v) {
    Node *n = malloc(sizeof(Node));
    n->val = v;
    n->next = head;
    head = n;
}

void pop(void) {
    if (!head) return;
    Node *tmp = head;
    head = head->next;
    free(tmp);
    /* use after free: reading tmp->val after free */
    printf("popped: %d\n", tmp->val);
}

int main(void) {
    push(42);
    push(7);
    pop();
    pop();
    return 0;
}
