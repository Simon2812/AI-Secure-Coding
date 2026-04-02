#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

static void read_number()
{
    char buf[32];
    int num = 0;

    if (fgets(buf, sizeof(buf), stdin) != NULL)
    {
        num = atoi(buf);
    }

    int squared = num * num;
    printf("%d\n", squared);

    return;
}

int main(void)
{
    read_number();
    return 0;
}