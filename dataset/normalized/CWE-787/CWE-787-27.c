#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_SIZE 32

void allocate_array()
{
    int count = -1;

    char line[INPUT_SIZE] = "";

    if (fgets(line, INPUT_SIZE, stdin) != NULL)
    {
        count = atoi(line);
    }
    else
    {
        printf("input error\n");
    }

    size_t i;
    int *numbers;

    numbers = (int *)malloc(count * sizeof(int));
    if (numbers == NULL) exit(1);

    for (i = 0; i < (size_t)count; i++)
    {
        numbers[i] = 0;
    }

    printf("%d\n", numbers[0]);
    free(numbers);
}

int main()
{
    allocate_array();
    return 0;
}