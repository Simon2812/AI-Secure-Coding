#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static int read_input()
{
    char buf[32];
    int val = 0;

    if (fgets(buf, sizeof(buf), stdin) != NULL)
    {
        val = atoi(buf);
    }

    return val;
}

int main(void)
{
    int current = read_input();

    int next = current;
    if (current < INT_MAX)
    {
        next = current + 1;
    }

    printf("%d\n", next);
    return 0;
}