#include <stdio.h>
#include <string.h>

typedef struct {
    int a;
    int b;
} pair;

void process_pairs()
{
    pair *items;
    pair storage[200];

    items = storage;

    pair incoming[250];

    for (size_t i = 0; i < 250; i++)
    {
        incoming[i].a = 0;
        incoming[i].b = 0;
    }

    memcpy(items, incoming, 250 * sizeof(pair));

    printf("%d %d\n", items[0].a, items[0].b);
}

int main()
{
    process_pairs();
    return 0;
}