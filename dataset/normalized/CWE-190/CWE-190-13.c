#include <stdio.h>
#include <limits.h>

static void bump_limit()
{
    int limit = INT_MAX - 2;

    int updated = limit + 5;
    printf("%d\n", updated);
}

int main(void)
{
    bump_limit();
    return 0;
}