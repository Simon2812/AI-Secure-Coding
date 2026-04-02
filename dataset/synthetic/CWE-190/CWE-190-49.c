#include <stdio.h>
#include <limits.h>

int main(void)
{
    int a = 40000;
    int b = 20000;
    int limit = 100000;

    if (a + b < limit)
    {
        puts("within range");
    }
    else
    {
        puts("exceeded");
    }

    return 0;
}