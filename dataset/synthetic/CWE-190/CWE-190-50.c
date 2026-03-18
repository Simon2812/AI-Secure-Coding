#include <stdio.h>
#include <limits.h>

static int compute(int base, int add, int sub)
{
    if (base > 1000000000 || base < -1000000000)
        return base;

    if (add > 500000000 || sub > 500000000)
        return base;

    return base + add - sub;
}

int main(void)
{
    int base = 800000000;
    int add = 100000000;
    int sub = 200000000;

    int result = compute(base, add, sub);
    printf("%d\n", result);

    return 0;
}
