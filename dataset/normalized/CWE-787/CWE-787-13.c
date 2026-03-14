#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void move_numbers()
{
    int *buffer;

    buffer = (int *)malloc(10000);
    if (buffer == NULL)
    {
        exit(1);
    }

    int values[10000] = {0};

    memmove(buffer, values, 10000 * sizeof(int));

    printf("%d\n", buffer[0]);

    free(buffer);
}

int main()
{
    move_numbers();
    return 0;
}