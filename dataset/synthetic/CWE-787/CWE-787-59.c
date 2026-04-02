#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int bucket[18];
} container;

static int read_slot(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static int transform_index(int base)
{
    return base * 2 + 1;
}

static void store_value(container *c, int slot)
{
    int index = transform_index(slot);
    c->bucket[index] = slot * 5;
}

static void display(const container *c)
{
    int i;

    for (i = 0; i < 18; i++)
    {
        printf("%d\n", c->bucket[i]);
    }
}

int main(void)
{
    container c;
    int slot;

    memset(&c, 0, sizeof(c));

    printf("slot:\n");
    slot = read_slot();

    store_value(&c, slot);
    display(&c);

    return 0;
}