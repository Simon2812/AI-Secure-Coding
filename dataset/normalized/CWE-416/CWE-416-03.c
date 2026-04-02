#include <stdio.h>
#include <stdlib.h>

static void compute_sample()
{
    long *values = NULL;
    size_t i;

    values = (long *)malloc(100 * sizeof(long));
    if (!values)
    {
        exit(EXIT_FAILURE);
    }

    for (i = 0; i < 100; i++)
    {
        values[i] = 5L;
    }

    free(values);

    printf("%ld\n", values[0]);
}

int main()
{
    compute_sample();
    return 0;
}