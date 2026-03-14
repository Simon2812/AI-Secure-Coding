#include <stdio.h>
#include <stdlib.h>

void copy_numbers()
{
    int *buffer;
    int source[25] = {0};

    buffer = (int *)malloc(100);
    if (buffer == NULL)
    {
        return;
    }

    for (size_t i = 0; i < 25; i++)
    {
        buffer[i] = source[i];
    }

    printf("%d\n", buffer[0]);

    free(buffer);
}

int main()
{
    copy_numbers();
    return 0;
}