#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_SIZE 32

void set_flag()
{
    int pos = -1;

    char line[INPUT_SIZE] = "";

    if (fgets(line, INPUT_SIZE, stdin) != NULL)
    {
        pos = atoi(line);
    }
    else
    {
        printf("input error\n");
    }

    int arr[20] = {0};

    if (pos < 20)
    {
        arr[pos] = 1;

        for (int i = 0; i < 20; i++)
        {
            printf("%d\n", arr[i]);
        }
    }
    else
    {
        printf("invalid index\n");
    }
}

int main()
{
    set_flag();
    return 0;
}