#include <stdio.h>
#include <stdlib.h>

static long compute_sum(const long *values)
{
    long total = 0;
    for (size_t pos = 0; pos < 4; ++pos)
    {
        total += values[pos];
    }
    return total;
}

static void process_batch()
{
    long *records = NULL;

    records = (long *)malloc(80 * sizeof(long));
    if (!records)
    {
        exit(EXIT_FAILURE);
    }

    for (size_t idx = 0; idx < 80; ++idx)
    {
        records[idx] = 5L;
    }

    long preview = records[0];

    int guard = 1;
    if (guard)
    {
        long result = compute_sum(records);
        printf("%ld:%ld\n", preview, result);
    }

    free(records);
}

int main()
{
    process_batch();
    return 0;
}