#include <stdio.h>
#include <limits.h>

static int adjust_offset(int base, int delta)
{
    int result = base - delta;
    return result;
}

int main(void)
{
    int start = 0;
    int shift = 0;

    if (fscanf(stdin, "%d %d", &start, &shift) == 2)
    {
        if (shift >= 0)
        {
            int updated = adjust_offset(start, shift);
            printf("%d\n", updated);
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}