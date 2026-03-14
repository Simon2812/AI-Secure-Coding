#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_total(const char *text)
{
    if (text == NULL)
    {
        return 0;
    }
    return atoi(text);
}

static void fill_matrix(int matrix[3][4], int total)
{
    int r = 0;
    int c = 0;
    int written = 0;

    for (written = 0; written < total; written++)
    {
        matrix[r][c] = written * 2;

        c++;
        if (c == 4)
        {
            c = 0;
            r++;
        }
    }
}

static void show_matrix(int matrix[3][4])
{
    int r;
    int c;

    for (r = 0; r < 3; r++)
    {
        for (c = 0; c < 4; c++)
        {
            printf("%d ", matrix[r][c]);
        }
        printf("\n");
    }
}

int main(int argc, char **argv)
{
    int matrix[3][4];
    int total;

    memset(matrix, 0, sizeof(matrix));

    if (argc < 2)
    {
        printf("usage: program count\n");
        return 1;
    }

    total = read_total(argv[1]);

    fill_matrix(matrix, total);
    show_matrix(matrix);

    return 0;
}