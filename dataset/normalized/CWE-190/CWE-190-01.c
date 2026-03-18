#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

static void process_input()
{
    int64_t value = 0;

    if (fscanf(stdin, "%" SCNd64, &value) != 1)
    {
        puts("input error");
        return;
    }

    int64_t squared = value * value;
    printf("%" PRId64 "\n", squared);
}

int main(void)
{
    process_input();
    return 0;
}