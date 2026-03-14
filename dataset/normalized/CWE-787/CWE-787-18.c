#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

void transfer_values()
{
    int64_t *buffer;

    buffer = (int64_t *)malloc(80 * sizeof(int64_t));
    if (buffer == NULL)
    {
        exit(1);
    }

    int64_t values[100] = {0};

    memmove(buffer, values, 100 * sizeof(int64_t));

    printf("%lld\n", (long long)buffer[0]);

    free(buffer);
}

int main()
{
    transfer_values();
    return 0;
}