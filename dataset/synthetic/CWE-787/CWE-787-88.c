#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char segment[32];
} block_area;

static int read_start(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void slide_copy(block_area *area, int start)
{
    char window[6];
    int i;

    for (i = 0; i < 6; i++)
    {
        window[i] = 'Q' + i;
    }

    if (start < 0)
    {
        return;
    }

    if (start >= (int)sizeof(area->segment))
    {
        return;
    }

    int remaining = sizeof(area->segment) - start;
    int limit = sizeof(window);

    if (limit > remaining)
    {
        limit = remaining;
    }

    for (i = 0; i < limit; i++)
    {
        area->segment[start + i] = window[i];
    }
}

static void print_segment(const block_area *area)
{
    int i;

    for (i = 0; i < (int)sizeof(area->segment); i++)
    {
        printf("%c\n", area->segment[i]);
    }
}

int main(void)
{
    block_area area;
    int start;

    memset(&area, 0, sizeof(area));

    printf("start:\n");
    start = read_start();

    slide_copy(&area, start);
    print_segment(&area);

    return 0;
}