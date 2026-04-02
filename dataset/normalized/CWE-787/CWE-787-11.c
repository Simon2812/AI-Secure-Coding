#include <stdio.h>
#include <stdlib.h>

void load_values()
{
    int *buffer;

    buffer = (int *)malloc(25);
    if (buffer == NULL)
    {
        exit(1);
    }

    int values[25] = {0};

    for (size_t i = 0; i < 25; i++)
    {
        buffer[i] = values[i];
    }

    printf("%d\n", buffer[0]);

    free(buffer);
}

int main()
{
    load_values();
    return 0;
}