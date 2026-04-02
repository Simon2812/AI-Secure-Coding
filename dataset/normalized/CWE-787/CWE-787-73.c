#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void copy_numbers()
{
    int64_t *data = (int64_t *)malloc(30 * sizeof(int64_t));
    if (data == NULL)
    {
        return;
    }

    int64_t source[30] = {0};

    memmove(data, source, 30 * sizeof(int64_t));

    printf("%lld\n", (long long)data[0]);

    free(data);
}

int main()
{
    copy_numbers();
    return 0;
}