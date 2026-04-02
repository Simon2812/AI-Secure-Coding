#include <stdio.h>
#include <limits.h>

typedef int (*handler_t)(int, int);

static int reduce_quota(int quota, int usage)
{
    int result = quota - usage;
    return result;
}

static int passthrough(int a, int b)
{
    return a;
}

static void execute(handler_t fn, int x, int y)
{
    int out = fn(x, y);
    printf("%d\n", out);
}

int main(void)
{
    handler_t table[2] = { reduce_quota, passthrough };

    int mode = 0;
    int quota = 2000000000;
    int usage = 1500000000;

    if (mode == 0)
        execute(table[0], quota, usage);
    else
        execute(table[1], quota, usage);

    return 0;
}