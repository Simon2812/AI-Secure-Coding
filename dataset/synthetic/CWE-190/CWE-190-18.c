#include <stdio.h>
#include <limits.h>

int main(void)
{
    int requests = 0;
    int i = 0;
    int total = 0;

    if (fscanf(stdin, "%d", &requests) == 1)
    {
        if (requests > 0 && requests < 100000)
        {
            for (i = 0; i < requests; i++)
            {
                total += 50000;
            }
            printf("%d\n", total);
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}