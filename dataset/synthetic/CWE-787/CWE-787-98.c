#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int ring[12];
    int cursor;
} ring_buffer;

static int read_events(void)
{
    char line[32];

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return 0;
    }

    return atoi(line);
}

static void push_value(ring_buffer *rb, int value)
{
    rb->ring[rb->cursor] = value;
    rb->cursor = (rb->cursor + 1) % 12;
}

static void simulate(ring_buffer *rb, int events)
{
    int i;

    if (events < 0)
    {
        return;
    }

    for (i = 0; i < events; i++)
    {
        push_value(rb, i * 4);
    }
}

static void dump_ring(const ring_buffer *rb)
{
    int i;

    for (i = 0; i < 12; i++)
    {
        printf("%d\n", rb->ring[i]);
    }
}

int main(void)
{
    ring_buffer rb;
    int events;

    memset(&rb, 0, sizeof(rb));

    printf("events:\n");
    events = read_events();

    simulate(&rb, events);
    dump_ring(&rb);

    return 0;
}