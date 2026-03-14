#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define INPUT_SIZE 32

void allocate_array()
{
    char inputBuffer[INPUT_SIZE];
    int count = 0;

    if (fgets(inputBuffer, INPUT_SIZE, stdin) == NULL)
    {
        printf("input failed\n");
        return;
    }

    count = atoi(inputBuffer);

    if (count <= 0)
    {
        printf("invalid size\n");
        return;
    }

    if ((size_t)count > SIZE_MAX / sizeof(int))
    {
        printf("size overflow detected\n");
        return;
    }

    int *buffer = (int *)malloc((size_t)count * sizeof(int));
    if (buffer == NULL)
    {
        printf("allocation failed\n");
        return;
    }

    for (size_t i = 0; i < (size_t)count; i++)
    {
        buffer[i] = 0;
    }

    printf("%d\n", buffer[0]);

    free(buffer);
}

int main()
{
    allocate_array();
    return 0;
}