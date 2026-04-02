#include <stdio.h>
#include <limits.h>

static int compute_remaining(int stock, int shipped)
{
    int remaining = stock - shipped;
    return remaining;
}

static void handle_batch(int initialStock)
{
    int shipped = 500000000;
    int current = initialStock;

    if (initialStock > 100)
    {
        current = compute_remaining(initialStock, shipped);
        printf("%d\n", current);
    }
    else
    {
        puts("small batch");
    }
}

int main(void)
{
    handle_batch(1200000000);
    return 0;
}