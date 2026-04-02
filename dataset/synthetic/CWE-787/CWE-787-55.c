#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char header[8];
    unsigned char body[24];
    unsigned char packet[28];
} builder;

static int read_header_len(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static int read_body_len(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void stitch_packet(builder *b, int head_len, int body_len)
{
    int cursor = 0;

    memcpy(b->packet + cursor, b->header, head_len);
    cursor += head_len;
    memcpy(b->packet + cursor, b->body, body_len);
}

static void show_packet(const builder *b)
{
    int i;

    for (i = 0; i < 28; i++)
    {
        printf("%u\n", b->packet[i]);
    }
}

int main(void)
{
    builder b;
    int head_len;
    int body_len;
    int i;

    memset(&b, 0, sizeof(b));

    for (i = 0; i < 8; i++)
    {
        b.header[i] = (unsigned char)(100 + i);
    }

    for (i = 0; i < 24; i++)
    {
        b.body[i] = (unsigned char)(10 + i);
    }

    printf("header length:\n");
    head_len = read_header_len();

    printf("body length:\n");
    body_len = read_body_len();

    stitch_packet(&b, head_len, body_len);
    show_packet(&b);

    return 0;
}