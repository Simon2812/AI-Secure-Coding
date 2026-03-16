#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
} Node;

static Node *cache[4];

static void store(int idx, Node *n)
{
    if (idx >= 0 && idx < 4)
        cache[idx] = n;
}

static void cleanup(Node *n)
{
    if (n)
    {
        if (n->data)
            free(n->data);
        free(n);
    }
}

static int inspect(Node *n)
{
    if (!n || !n->data)
        return 0;

    return (int)strlen(n->data);
}

int main(void)
{
    Node *entry = (Node *)malloc(sizeof(Node));
    if (!entry)
        return 1;

    entry->data = (char *)malloc(32);
    if (!entry->data)
    {
        free(entry);
        return 1;
    }

    strcpy(entry->data, "cached_value");

    store(1, entry);

    cleanup(entry);

    Node *alias = cache[1];

    int var = inspect(alias);

    return 0;
}