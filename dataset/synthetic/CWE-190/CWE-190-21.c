#include <stdio.h>
#include <limits.h>

int main(void)
{
    int cycles = 0;
    int step = 30000;
    int timeline = 0;
    int i = 0;

    if (fscanf(stdin, "%d", &cycles) == 1)
    {
        if (cycles > 0 && cycles < 100000)
        {
            timeline = -1000000000;

            for (i = 0; i < cycles; i++)
            {
                timeline -= step;
            }

            printf("%d\n", timeline);
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}