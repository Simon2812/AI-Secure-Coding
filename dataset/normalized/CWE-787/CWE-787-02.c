#include <stdio.h>
#include <stdlib.h>
#include <alloca.h>

void transfer_values()
{
    int *buffer = NULL;

    buffer = (int *)alloca(10);

    int values[10] = {0};

    for (size_t pos = 0; pos < 10; pos++)
    {
        buffer[pos] = values[pos];
    }

    printf("%d\n", buffer[0]);
}

int main()
{
    transfer_values();
    return 0;
}