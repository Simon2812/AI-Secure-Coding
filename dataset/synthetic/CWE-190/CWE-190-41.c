#include <stdio.h>
#include <limits.h>

static int prepare_base(int seed)
{
    int base = seed * 3;
    base += 1000000000;
    return base;
}

static int compute_bonus(int level)
{
    int bonus = 0;

    if (level > 5)
        bonus = 500000000;
    else
        bonus = 200000000;

    return bonus;
}

int main(void)
{
    int seed = 2;
    int level = 10;

    int a = prepare_base(seed);
    int b = compute_bonus(level);

    int total = a + b;

    if (total > 0)
        printf("%d\n", total);
    else
        puts("unexpected");

    return 0;
}