#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int columns[16];
} column_buffer;

static int read_column(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return -1;
    }

    return atoi(buf);
}

static int read_value(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void write_column(column_buffer *cb, int column)
{
    int row;

    for (row = 0; row < 4; row++)
    {
        int index = row * 4 + column;
        cb->columns[index] = read_value();
    }
}

static void dump_columns(const column_buffer *cb)
{
    int i;

    for (i = 0; i < 16; i++)
    {
        printf("%d\n", cb->columns[i]);
    }
}

int main(void)
{
    column_buffer cb;
    int column;

    memset(&cb, 0, sizeof(cb));

    printf("column index:\n");

    column = read_column();

    write_column(&cb, column);
    dump_columns(&cb);

    return 0;
}