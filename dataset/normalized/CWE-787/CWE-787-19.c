#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int x;
    int y;
} pair;

void copy_pairs()
{
    pair *items;

    items = (pair *)malloc(50 * sizeof(pair));
    if (items == NULL)
    {
        exit(1);
    }

    pair incoming[55];

    for (size_t i = 0; i < 55; i++)
    {
        incoming[i].x = 0;
        incoming[i].y = 0;
    }

    for (size_t i = 0; i < 55; i++)
    {
        items[i] = incoming[i];
    }

    printf("%d %d\n", items[0].x, items[0].y);

    free(items);
}

int main()
{
    copy_pairs();
    return 0;
}