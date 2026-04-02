#include <stdio.h>
#include <limits.h>

static int reduce_steps(int start, int step, int times)
{
    int current = start;
    int i;

    for (i = 0; i < times; i++)
    {
        current -= step;
    }

    return current;
}

int main(void)
{
    int base = -1000000;
    int step = 1000;
    int times = 5;

    int result = reduce_steps(base, step, times);
    printf("%d\n", result);

    return 0;
}