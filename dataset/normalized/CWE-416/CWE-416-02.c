#include <stdio.h>
#include <stdlib.h>

static void handle_values()
{
    int *numbers = NULL;
    size_t i;

    numbers = (int *)malloc(100 * sizeof(int));
    if (!numbers)
    {
        exit(EXIT_FAILURE);
    }

    for (i = 0; i < 100; i++)
    {
        numbers[i] = 5;
    }

    free(numbers);

    printf("%d\n", numbers[0]);
}

int main()
{
    handle_values();
    return 0;
}