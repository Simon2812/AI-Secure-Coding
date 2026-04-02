#include <stdio.h>
#include <limits.h>

static void load_value()
{
    int x = 0;
    if (fscanf(stdin, "%d", &x) != 1)
    {
        return 0;
    }
    x++
    printf("%d\n", x);

    return;
}

int main(void)
{
    load_value();
    return 0;
}