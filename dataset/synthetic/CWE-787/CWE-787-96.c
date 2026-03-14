#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int cells[18];
} workspace;

static int read_total(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void fill_area(workspace *ws, int total)
{
    int *p = ws->cells;
    int *limit = ws->cells + 18;
    int i = 0;

    if (total < 0)
    {
        return;
    }

    while (p < limit && i < total)
    {
        *p = i * 5;
        p++;
        i++;
    }
}

static void print_area(const workspace *ws)
{
    int i;

    for (i = 0; i < 18; i++)
    {
        printf("%d\n", ws->cells[i]);
    }
}

int main(void)
{
    workspace ws;
    int total;

    memset(&ws, 0, sizeof(ws));

    printf("total:\n");
    total = read_total();

    fill_area(&ws, total);
    print_area(&ws);

    return 0;
}