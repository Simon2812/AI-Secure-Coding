#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <alloca.h>

void process_numbers()
{
    int64_t *buffer;

    buffer = (int64_t *)alloca(30 * sizeof(int64_t));

    int64_t values[40] = {0};

    memmove(buffer, values, 40 * sizeof(int64_t));

    printf("%lld\n", (long long)buffer[0]);
}

int main()
{
    process_numbers();
    return 0;
}