#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int capacity;
    int *entries;
} buffer_pool;

static int read_amount(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void allocate_pool(buffer_pool *p, int amount)
{
    int i;

    if (amount < 0)
    {
        amount = 0;
    }

    p->capacity = amount;
    p->entries = (int *)malloc(sizeof(int) * p->capacity);

    if (p->entries == NULL)
    {
        p->capacity = 0;
        return;
    }

    for (i = 0; i < p->capacity; i++)
    {
        p->entries[i] = i * 3;
    }
}

static void display_pool(const buffer_pool *p)
{
    int i;

    for (i = 0; i < p->capacity; i++)
    {
        printf("%d\n", p->entries[i]);
    }
}

int main(void)
{
    buffer_pool p;
    int amount;

    p.capacity = 0;
    p.entries = NULL;

    printf("amount:\n");
    amount = read_amount();

    allocate_pool(&p, amount);
    display_pool(&p);

    free(p.entries);

    return 0;
}