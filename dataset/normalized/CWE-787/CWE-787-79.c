#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>

void allocate_numbers()
{
    int count = rand();

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

    int *numbers = (int *)malloc((size_t)count * sizeof(int));
    if (numbers == NULL)
    {
        printf("allocation failed\n");
        return;
    }

    for (size_t i = 0; i < (size_t)count; i++)
    {
        numbers[i] = 0;
    }

    printf("%d\n", numbers[0]);

    free(numbers);
}

int main()
{
    srand((unsigned)time(NULL));
    allocate_numbers();
    return 0;
}