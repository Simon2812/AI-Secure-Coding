#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int matrix[4][4];
} table_block;

static int read_column(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void update_column(table_block *tb, int column)
{
    int row;

    if (column < 0)
    {
        return;
    }

    column = column % 4;

    for (row = 0; row < 4; row++)
    {
        tb->matrix[row][column] = row * 10 + column;
    }
}

static void print_table(const table_block *tb)
{
    int r;
    int c;

    for (r = 0; r < 4; r++)
    {
        for (c = 0; c < 4; c++)
        {
            printf("%d\n", tb->matrix[r][c]);
        }
    }
}

int main(void)
{
    table_block tb;
    int column;

    memset(&tb, 0, sizeof(tb));

    printf("column:\n");
    column = read_column();

    update_column(&tb, column);
    print_table(&tb);

    return 0;
}