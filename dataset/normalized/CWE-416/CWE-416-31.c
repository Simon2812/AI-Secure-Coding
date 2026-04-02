#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void render_item()
{
    char *segment = NULL;

    segment = (char *)malloc(96);
    if (!segment)
    {
        exit(EXIT_FAILURE);
    }

    memset(segment, 'A', 95);
    segment[95] = '\0';

    int marker = 1;

    if (marker)
    {
        puts(segment);
    }

    free(segment);
}

int main()
{
    render_item();
    return 0;
}