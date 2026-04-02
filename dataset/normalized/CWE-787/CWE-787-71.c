#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void transfer_values()
{
    int *buffer;
    int source[20] = {0};

    buffer = (int *)malloc(20 * sizeof(int));
    if (buffer == NULL)
    {
        return;
    }

    memcpy(buffer, source, 20 * sizeof(int));

    printf("%d\n", buffer[0]);

    free(buffer);
}

int main()
{
    transfer_values();
    return 0;
}