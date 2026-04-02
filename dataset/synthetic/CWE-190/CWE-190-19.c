#include <stdio.h>
#include <limits.h>

int main(void)
{
    int units = 0;
    int batchSize = 0;
    int capacity = 0;

    if (fscanf(stdin, "%d %d", &units, &batchSize) == 2)
    {
        if (units > 0 && batchSize > 0)
        {
            if (batchSize < 10000)
            {
                capacity = units * batchSize;
                printf("%d\n", capacity);
            }
            else
            {
                puts("batch too large");
            }
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}