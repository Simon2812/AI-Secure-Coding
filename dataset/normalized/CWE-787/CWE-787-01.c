#include <stdio.h>
#include <stdlib.h>

#define INPUT_BUF 32

void process_request()
{
    int index = -1;

    char line[INPUT_BUF];
    if (fgets(line, sizeof(line), stdin) != NULL)
    {
        index = atoi(line);
    }
    else
    {
        puts("input error");
    }

    int values[10] = {0};

    if (index >= 0)
    {
        values[index] = 1;

        for (int k = 0; k < 10; k++)
        {
            printf("%d\n", values[k]);
        }
    }
    else
    {
        puts("invalid index");
    }
}

int main()
{
    process_request();
    return 0;
}