#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int slots[15];
} store_unit;

static int read_base(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void scatter(store_unit *unit, int base)
{
    int step;

    if (base < 0)
    {
        return;
    }

    for (step = 0; step < 5; step++)
    {
        int pos = base + step * 2;

        if (pos >= 15)
        {
            break;
        }

        unit->slots[pos] = pos * 6;
    }
}

static void print_store(const store_unit *unit)
{
    int i;

    for (i = 0; i < 15; i++)
    {
        printf("%d\n", unit->slots[i]);
    }
}

int main(void)
{
    store_unit unit;
    int base;

    memset(&unit, 0, sizeof(unit));

    printf("base:\n");
    base = read_base();

    scatter(&unit, base);
    print_store(&unit);

    return 0;
}