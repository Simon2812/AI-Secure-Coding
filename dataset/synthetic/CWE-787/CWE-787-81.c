#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_total(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void fill_board(int *board, int size, int total)
{
    int i;
    int limit = total;

    if (limit > size)
    {
        limit = size;
    }

    if (limit < 0)
    {
        limit = 0;
    }

    for (i = 0; i < limit; i++)
    {
        board[i] = (i + 1) * 4;
    }
}

static void print_board(const int *board, int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("%d\n", board[i]);
    }
}

int main(void)
{
    int board[8];
    int total;

    memset(board, 0, sizeof(board));

    printf("count:\n");
    total = read_total();

    fill_board(board, 8, total);
    print_board(board, 8);

    return 0;
}