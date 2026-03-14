#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char payload[40];
} packet;

static int read_length(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void emit_chunk(packet *p, int length)
{
    char source[20];
    int i;

    for (i = 0; i < (int)sizeof(source); i++)
    {
        source[i] = 'a' + i;
    }

    size_t n = length;

    if (n > sizeof(source))
    {
        n = sizeof(source);
    }

    if (n > sizeof(p->payload))
    {
        n = sizeof(p->payload);
    }

    memcpy(p->payload, source, n);
}

static void inspect_packet(const packet *p)
{
    int i;

    for (i = 0; i < (int)sizeof(p->payload); i++)
    {
        printf("%c\n", p->payload[i]);
    }
}

int main(void)
{
    packet p;
    int length;

    memset(&p, 0, sizeof(p));

    printf("length:\n");
    length = read_length();

    emit_chunk(&p, length);
    inspect_packet(&p);

    return 0;
}