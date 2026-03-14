#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void update_entry()
{
    int index = rand();

    int *buffer = (int *)malloc(15 * sizeof(int));
    if (buffer == NULL)
    {
        return;
    }

    for (int i = 0; i < 15; i++)
    {
        buffer[i] = 0;
    }

    if (index >= 0 && index < 15)
    {
        buffer[index] = 1;

        for (int i = 0; i < 15; i++)
        {
            printf("%d\n", buffer[i]);
        }
    }
    else
    {
        printf("index out of bounds\n");
    }

    free(buffer);
}

int main()
{
    srand((unsigned)time(NULL));
    update_entry();
    return 0;
}