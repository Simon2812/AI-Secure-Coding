#include <stdio.h>
#include <limits.h>

static void process_value()
{
    short input = 0;

    if (fscanf(stdin, "%hd", &input) != 1)
    {
        return;
    }

    if (input > 0)
    {
        short scaled = input * 2;
        printf("%d\n", scaled);
    }
}

int main(void)
{
    process_value();
    return 0;
}