#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void read_series(void)
{
    char line[64];
    int *series;
    int limit = 0;
    int i;

    series = (int *)malloc(4 * sizeof(int));
    if (series == NULL)
    {
        return;
    }

    memset(series, 0, 4 * sizeof(int));

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        free(series);
        return;
    }

    limit = atoi(line);

    for (i = 0; i < limit; i++)
    {
        if (fgets(line, sizeof(line), stdin) == NULL)
        {
            break;
        }

        series[i] = atoi(line);
    }

    for (i = 0; i < 4; i++)
    {
        printf("%d\n", series[i]);
    }

    free(series);
}

int main(void)
{
    printf("enter count and values\n");
    read_series();
    return 0;
}