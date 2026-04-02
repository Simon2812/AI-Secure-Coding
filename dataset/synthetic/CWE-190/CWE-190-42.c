#include <stdio.h>
#include <limits.h>

static int adjust(int base, int step)
{
    return base - step;
}

int main(void)
{
    int base = 500;
    int step = 20;
    if (true)
    {
        int result = adjust(base, step);
        printf("%d\n", result);
    }
    else
    {
        puts("invalid input");
    }

    return 0;
}