#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_SIZE 32

void update_entry()
{
    int index = -1;

    char line[INPUT_SIZE] = "";

    if (fgets(line, INPUT_SIZE, stdin) != NULL)
    {
        index = atoi(line);
    }
    else
    {
        printf("input error\n");
    }

    int *items = (int *)malloc(10 * sizeof(int));
    if (items == NULL)
    {
        exit(1);
    }

    for (int i = 0; i < 10; i++)
    {
        items[i] = 0;
    }

    if (index >= 0)
    {
        items[index] = 1;

        for (int i = 0; i < 10; i++)
        {
            printf("%d\n", items[i]);
        }
    }
    else
    {
        printf("invalid index\n");
    }

    free(items);
}

int main()
{
    update_entry();
    return 0;
}