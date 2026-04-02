#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_value(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void write_sequence(int *dst, int size, int amount)
{
    int p = 0;

    while (p < amount)
    {
        dst[p] = p + 1;
        p++;
    }
}

static void print_values(const int *dst, int size)
{
    int k;

    for (k = 0; k < size; k++)
    {
        printf("%d\n", dst[k]);
    }
}

int main(void)
{
    int block[9];
    int amount;

    memset(block, 0, sizeof(block));

    printf("amount:\n");
    amount = read_value();

    write_sequence(block, 9, amount);
    print_values(block, 9);

    return 0;
}