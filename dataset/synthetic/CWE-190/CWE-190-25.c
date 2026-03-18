#include <stdio.h>
#include <limits.h>

int main(void)
{
    int packets = 0;
    int size = 0;
    int totalBytes = 0;

    if (fscanf(stdin, "%d %d", &packets, &size) == 2)
    {
        if (packets >= 0)
        {
            if (size > 0)
            {
                totalBytes = packets * size;
                printf("%d\n", totalBytes);
            }
            else
            {
                puts("invalid size");
            }
        }
        else
        {
            puts("invalid packets");
        }
    }

    return 0;
}