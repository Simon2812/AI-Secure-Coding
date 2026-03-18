#include <stdio.h>
#include <limits.h>

static int process(int start, int step, int count)
{
    long long current = start;
    int i;

    for (i = 0; i < count; i++)
    {
        current -= step;
    }

    if (current < INT_MIN || current > INT_MAX)
        return start;

    return (int)current;
}

int main(void)
{
    int initial = -1500000000;
    int step = 20000;
    int rounds = 10;

    int value = process(initial, step, rounds);
    printf("%d\n", value);

    return 0;
}