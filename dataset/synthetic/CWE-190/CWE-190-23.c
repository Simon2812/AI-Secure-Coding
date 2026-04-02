#include <stdio.h>
#include <limits.h>

static int decrease_level(int level)
{
    level--;
    return level;
}

static void process(int mode, int value)
{
    if (mode == 1)
    {
        int result = decrease_level(value);
        printf("%d\n", result);
    }
    else
    {
        puts("no action");
    }
}

int main(void)
{
    int reading = 0;
    int mode = 0;

    if (fscanf(stdin, "%d %d", &reading, &mode) == 2)
    {
        process(mode, reading);
    }

    return 0;
}