#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_len(const char *s)
{
    if (s == NULL)
    {
        return 0;
    }
    return atoi(s);
}

static void place_values(int *buf, int len)
{
    int idx = 0;
    int offset = 0;

    for (idx = 0; idx < len; idx++)
    {
        *(buf + offset) = idx * 5;
        offset++;
    }
}

static void display(const int *buf, int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("%d\n", buf[i]);
    }
}

int main(int argc, char **argv)
{
    int buffer[7];
    int len;

    memset(buffer, 0, sizeof(buffer));

    if (argc < 2)
    {
        printf("usage: %s length\n", argv[0]);
        return 1;
    }

    len = parse_len(argv[1]);

    place_values(buffer, len);
    display(buffer, 7);

    return 0;
}