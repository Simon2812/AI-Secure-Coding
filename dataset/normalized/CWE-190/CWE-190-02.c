#include <stdio.h>
#include <limits.h>

static void compute()
{
    short input = SHRT_MAX;

    short output = input * input;
    printf("%d\n", output);
}

int main(void)
{
    compute();
    return 0;
}