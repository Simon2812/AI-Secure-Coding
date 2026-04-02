#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int get_amount(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void fill_buffer(char *dst, int amount)
{
    int i;

    for (i = 0; i < amount; i++)
    {
        *(dst + i) = 'A';
    }
}

static void print_buffer(const char *dst, int size)
{
    int j;

    for (j = 0; j < size; j++)
    {
        putchar(dst[j]);
    }

    putchar('\n');
}

int main(void)
{
    char area[10];
    int amount;

    memset(area, 0, sizeof(area));

    printf("amount:\n");
    amount = get_amount();

    fill_buffer(area, amount);
    print_buffer(area, 10);

    return 0;
}