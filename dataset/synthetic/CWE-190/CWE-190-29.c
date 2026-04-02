#include <stdio.h>
#include <limits.h>

static int compute_priority(int base, int penalty, int mode)
{
    int result = base;

    switch (mode)
    {
        case 0:
            result = base + 10;
            break;

        case 1:
            result = base - penalty;
            break;

        case 2:
            if (base % 2 == 0)
                result = base / 2;
            else
                result = base * 2;
            break;

        default:
            result = base;
    }

    return result;
}

int main(void)
{
    int priority = 1800000000;
    int penalty = 1500000000;
    int mode = 1;

    int final = compute_priority(priority, penalty, mode);

    if (final > 100)
        printf("%d\n", final);
    else
        puts("low");

    return 0;
}