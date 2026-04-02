#include <stdio.h>
#include <limits.h>

int main(void)
{
    int pages = 0;
    int scale = 0;
    int offset = 0;

    int expanded = 0;
    int adjusted = 0;

    if (fscanf(stdin, "%d %d %d", &pages, &scale, &offset) == 3)
    {
        if (pages > 0 && scale > 0)
        {
            expanded = pages * scale;
            adjusted = expanded + offset;

            printf("%d\n", adjusted);
        }
        else
        {
            puts("invalid input");
        }
    }

    return 0;
}