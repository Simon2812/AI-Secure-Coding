#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int cells[12];
} grid_area;

static int read_position(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void apply_value(grid_area *g, int pos)
{
    int index;

    if (pos < 0)
    {
        return;
    }

    index = pos % 12;
    g->cells[index] = pos * 2;
}

static void print_grid(const grid_area *g)
{
    int i;

    for (i = 0; i < 12; i++)
    {
        printf("%d\n", g->cells[i]);
    }
}

int main(void)
{
    grid_area g;
    int pos;

    memset(&g, 0, sizeof(g));

    printf("position:\n");
    pos = read_position();

    apply_value(&g, pos);
    print_grid(&g);

    return 0;
}