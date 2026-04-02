#include <stdio.h>
#include <limits.h>

int main(void)
{
    int balance = 0;
    int deduction = 0;
    int remaining = 0;

    if (fscanf(stdin, "%d %d", &balance, &deduction) == 2)
    {
        if (balance < 0)
        {
            puts("negative balance not allowed");
        }
        else if (deduction < 0)
        {
            puts("invalid deduction");
        }
        else if (deduction == 0)
        {
            printf("%d\n", balance);
        }
        else
        {
            remaining = balance - deduction;
            printf("%d\n", remaining);
        }
    }

    return 0;
}