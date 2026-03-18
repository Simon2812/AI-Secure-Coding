#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void compute_random()
{
    int v = rand();

    int out = v * v;
    printf("%d\n", out);
}

int main(void)
{
    srand((unsigned)time(NULL));
    compute_random();
    return 0;
}