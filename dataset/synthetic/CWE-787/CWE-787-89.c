#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char frame[28];
} packet_frame;

static int read_head(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static int read_tail(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void assemble(packet_frame *p, int head_len, int tail_len)
{
    unsigned char head[10];
    unsigned char tail[10];
    int cursor = 0;
    int i;

    for (i = 0; i < 10; i++)
    {
        head[i] = (unsigned char)(50 + i);
        tail[i] = (unsigned char)(80 + i);
    }

    if (head_len < 0)
    {
        head_len = 0;
    }

    if (tail_len < 0)
    {
        tail_len = 0;
    }

    if (head_len > (int)sizeof(head))
    {
        head_len = sizeof(head);
    }

    if (tail_len > (int)sizeof(tail))
    {
        tail_len = sizeof(tail);
    }

    if (head_len + tail_len > (int)sizeof(p->frame))
    {
        tail_len = sizeof(p->frame) - head_len;
    }

    memcpy(p->frame + cursor, head, head_len);
    cursor += head_len;

    memcpy(p->frame + cursor, tail, tail_len);
}

static void print_frame(const packet_frame *p)
{
    int i;

    for (i = 0; i < (int)sizeof(p->frame); i++)
    {
        printf("%u\n", p->frame[i]);
    }
}

int main(void)
{
    packet_frame p;
    int head_len;
    int tail_len;

    memset(&p, 0, sizeof(p));

    printf("head length:\n");
    head_len = read_head();

    printf("tail length:\n");
    tail_len = read_tail();

    assemble(&p, head_len, tail_len);
    print_frame(&p);

    return 0;
}