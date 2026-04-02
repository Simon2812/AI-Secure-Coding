#include <stdio.h>
#include <stdlib.h>

void write_value()
{
    int ind = -5;

    int arr[10] = {0};

    if (ind < 10)
    {
        arr[ind] = 1;

        for (int i = 0; i < 10; i++)
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
    write_value();
    return 0;
}