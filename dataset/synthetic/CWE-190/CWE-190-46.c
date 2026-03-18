#include <stdio.h>
#include <limits.h>

static int transform(int mode, int base)
{
    int result;

    switch (mode)
    {
        case 0:
            result = base - 10;
            break;

        case 1:
            result = base - 20;
            break;

        case 2:
            result = base - 30;
            break;

        default:
            result = base;
    }

    return result;
}

int main(void)
{
    int value = -500;
    int mode = 1;

    int out = transform(mode, value);
    printf("%d\n", out);

    return 0;
}