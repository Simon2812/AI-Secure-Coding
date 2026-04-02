#include <stdio.h>
#include <stdlib.h>

static int next_value(void)
{
    char tmp[32];

    if (fgets(tmp, sizeof(tmp), stdin) == NULL)
    {
        return -1;
    }

    return atoi(tmp);
}

static void insert_pair(int *table, int pos, int value)
{
    table[pos] = value;
    table[pos + 1] = value + 1;
}

static void build_pairs(int *table, int capacity)
{
    int start;

    while (1)
    {
        start = next_value();

        if (start < 0)
        {
            break;
        }

        insert_pair(table, start, start * 3);
    }
}

static void show_table(const int *table, int capacity)
{
    int i;

    for (i = 0; i < capacity; i++)
    {
        printf("%d\n", table[i]);
    }
}

int main(void)
{
    int table[10] = {0};

    printf("enter indexes (negative to stop)\n");

    build_pairs(table, 10);
    show_table(table, 10);

    return 0;
}