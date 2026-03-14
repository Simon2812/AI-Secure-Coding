#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char payload[40];
} message;

static int read_offset(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return -1;
    }

    return atoi(line);
}

static void scatter_write(message *m, int base)
{
    int step;

    for (step = 0; step < 5; step++)
    {
        int pos = base + step * 7;
        m->payload[pos] = (unsigned char)(pos & 0xFF);
    }
}

static void dump(const message *m)
{
    int i;

    for (i = 0; i < 40; i++)
    {
        printf("%u\n", m->payload[i]);
    }
}

int main(void)
{
    message m;
    int offset;

    memset(&m, 0, sizeof(m));

    printf("offset:\n");
    offset = read_offset();

    scatter_write(&m, offset);
    dump(&m);

    return 0;
}