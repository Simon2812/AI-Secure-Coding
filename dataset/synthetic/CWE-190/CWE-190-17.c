#include <stdio.h>
#include <limits.h>

int main(void)
{
    int charge = 0;
    int extra = 0;

    if (fscanf(stdin, "%d %d", &charge, &extra) == 2)
    {
        if (charge >= 0 && extra >= 0)
        {
            int total = charge + extra;
            printf("%d\n", total);
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}