#include <stdio.h>
#include <stdlib.h>

void update_slot()
{
    int value = -1;

    char inputBuffer[32] = "";

    if (fgets(inputBuffer, sizeof(inputBuffer), stdin) != NULL)
    {
        value = atoi(inputBuffer);
    }
    else
    {
        printf("input failed\n");
    }

    int buffer[10] = {0};

    if (value >= 0 && value < 10)
    {
        buffer[value] = 1;

        for (int i = 0; i < 10; i++)
        {
            printf("%d\n", buffer[i]);
        }
    }
    else
    {
        printf("index out of range\n");
    }
}

int main()
{
    update_slot();
    return 0;
}