#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_numbers()
{
    int *arr;

    arr = (int *)malloc(120);
    if (arr == NULL)
    {
        exit(1);
    }

    int values[120] = {0};

    memcpy(arr, values, 120 * sizeof(int));

    printf("%d\n", arr[0]);

    free(arr);
}

int main()
{
    copy_numbers();
    return 0;
}