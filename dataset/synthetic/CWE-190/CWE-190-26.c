#include <stdio.h>
#include <limits.h>

int main(void)
{
    int price = 0;
    int discount = 0;

    if (fscanf(stdin, "%d %d", &price, &discount) != 2)
        return 0;

    if (price < 0)
        return 0;

    printf("%d\n", price - discount);

    return 0;
}