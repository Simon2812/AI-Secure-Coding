#include <stdio.h>
#include <limits.h>

int main(void)
{
    int start = -1200000000;
    int offset = 300000000;

    int temp = -offset;
    int result = start + temp;

    printf("%d\n", result);

    return 0;
}