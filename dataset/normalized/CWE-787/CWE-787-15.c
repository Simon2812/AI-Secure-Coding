#include <stdio.h>
#include <stdlib.h>

void mark_position()
{
    int idx = rand();

    int *arr = (int *)malloc(100 * sizeof(int));
    if (arr == NULL)
    {
        exit(1);
    }

    for (int i = 0; i < 100; i++)
    {
        arr[i] = 0;
    }

    if (idx >= 0)
    {
        arr[idx] = 1;

        for (int i = 0; i < 100; i++)
        {
            printf("%d\n", arr[i]);
        }
    }
    else
    {
        printf("invalid index\n");
    }

    free(arr);
}

int main()
{
    mark_position();
    return 0;
}