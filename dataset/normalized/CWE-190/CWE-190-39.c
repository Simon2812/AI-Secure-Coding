#include <stdio.h>
#include <limits.h>

static void compute()
{
    int input = 0;

    if (fscanf(stdin, "%d", &input) == 1)
    {
        if (input > 0 && input <= INT_MAX / 2)
        {
            int result = input * 2;
            printf("%d\n", result);
        }
        else
        {
            puts("input out of safe range");
        }
    }
}

int main(void)
{
    compute();
    return 0;
}