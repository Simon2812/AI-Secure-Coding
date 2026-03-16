#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

static Node *append(Node *head, int v)
{
    Node *n = (Node *)malloc(sizeof(Node));
    if (!n)
        return head;

    n->value = v;
    n->next = NULL;

    if (!head)
        return n;

    Node *cur = head;
    while (cur->next)
        cur = cur->next;

    cur->next = n;
    return head;
}

static void drop(Node *n)
{
    if (n)
        free(n);
}

static int read_value(Node *n)
{
    return n->value;
}

int main(void)
{
    Node *head = NULL;

    head = append(head, 10);
    head = append(head, 20);

    Node *external = head->next;

    drop(head->next);

    int result = read_value(external);

    printf("%d\n", result);

    free(head);

    return 0;
}