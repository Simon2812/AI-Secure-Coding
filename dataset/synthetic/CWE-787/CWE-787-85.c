#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int store[10];
} ledger;

static int read_total(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void populate(ledger *l, int total)
{
    int *cursor = l->store;
    int *end = l->store + 10;
    int i = 0;

    while (cursor < end && i < total)
    {
        *cursor = i * 7;
        cursor++;
        i++;
    }
}

static void show(const ledger *l)
{
    int i;

    for (i = 0; i < 10; i++)
    {
        printf("%d\n", l->store[i]);
    }
}

int main(void)
{
    ledger l;
    int total;

    memset(&l, 0, sizeof(l));

    printf("total:\n");
    total = read_total();

    populate(&l, total);
    show(&l);

    return 0;
}