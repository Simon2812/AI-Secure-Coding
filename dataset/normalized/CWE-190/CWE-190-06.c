#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void recalc_capacity()
{
    unsigned int capacity = (unsigned int)(rand());

    if (capacity > 0)
    {
        unsigned int expanded = capacity * 4;
        printf("%u\n", expanded);
    }
}

int main(void)
{
    srand((unsigned)time(NULL));
    recalc_capacity();
    return 0;
}