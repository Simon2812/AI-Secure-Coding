#include <stdio.h>
#include <limits.h>

static void update_counter()
{
    unsigned int counter = UINT_MAX;

    unsigned int next = counter + 100;
    printf("%u\n", next);
}

int main(void)
{
    update_counter();
    return 0;
}