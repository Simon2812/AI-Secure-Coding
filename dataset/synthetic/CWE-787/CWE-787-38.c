#include <stdio.h>
#include <stdlib.h>

static int get_position(const char *text)
{
    if (text == NULL)
    {
        return 0;
    }
    return atoi(text);
}

static void write_value(int *buffer, int pos)
{
    buffer[pos] = 500;
}

static void show_buffer(int *buffer, int size)
{
    int j;

    for (j = 0; j < size; j++)
    {
        printf("%d\n", buffer[j]);
    }
}

int main(int argc, char **argv)
{
    int cells[5] = {11, 22, 33, 44, 55};
    int pos;

    if (argc < 2)
    {
        printf("need index\n");
        return 1;
    }

    pos = get_position(argv[1]);

    write_value(cells, pos);
    show_buffer(cells, 5);

    return 0;
}