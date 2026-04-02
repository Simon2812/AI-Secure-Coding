#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int cells[6];
} grid;

static int read_row(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return -1;
    }

    return atoi(buf);
}

static int read_col(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return -1;
    }

    return atoi(buf);
}

static void place_value(grid *g, int row, int col)
{
    int index = row * 3 + col;
    g->cells[index] = row + col;
}

static void show_grid(const grid *g)
{
    int i;

    for (i = 0; i < 6; i++)
    {
        printf("%d\n", g->cells[i]);
    }
}

int main(void)
{
    grid g;
    int row;
    int col;

    memset(&g, 0, sizeof(g));

    printf("row:\n");
    row = read_row();

    printf("col:\n");
    col = read_col();

    place_value(&g, row, col);
    show_grid(&g);

    return 0;
}