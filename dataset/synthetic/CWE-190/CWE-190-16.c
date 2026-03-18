#include <stdio.h>
#include <limits.h>

static void print_archive_size(int pages)
{
    int bytes = pages * 4096;
    printf("%d\n", bytes);
}

int main(void)
{
    int pages = 0;

    if (fscanf(stdin, "%d", &pages) == 1)
    {
        if (pages > 0)
        {
            print_archive_size(pages);
        }
        else
        {
            puts("pages must be positive");
        }
    }

    return 0;
}