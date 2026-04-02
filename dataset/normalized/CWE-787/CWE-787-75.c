#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_SIZE 32

void update_array()
{
    int index = -1;
    char inputBuffer[INPUT_SIZE];

    if (fgets(inputBuffer, INPUT_SIZE, stdin) != NULL)
    {
        index = atoi(inputBuffer);
    }
    else
    {
        printf("input failed\n");
        return;
    }

    int buffer[10] = {0};

    if (index >= 0 && index < 10)
    {
        buffer[index] = 1;

        for (int i = 0; i < 10; i++)
        {
            printf("%d\n", buffer[i]);
        }
    }
    else
    {
        printf("index out of bounds\n");
    }
}

int main()
{
    update_array();
    return 0;
}