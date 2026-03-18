#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <limits.h>

static void update_total()
{
    int64_t total = (int64_t)rand();

    int64_t next = total;
    if (total < LLONG_MAX - 1)
    {
        next = total + 2;
    }

    printf("%lld\n", (long long)next);
}

int main(void)
{
    srand((unsigned)time(NULL));
    update_total();
    return 0;
}