#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int data[12];
    int head;
} ring_buffer;

static int read_step(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return -1;
    }

    return atoi(buf);
}

static void push_many(ring_buffer *rb)
{
    int step;

    while (1)
    {
        step = read_step();

        if (step < 0)
        {
            break;
        }

        rb->head += step;
        rb->data[rb->head] = step * 2;
    }
}

static void show(const ring_buffer *rb)
{
    int i;

    for (i = 0; i < 12; i++)
    {
        printf("%d\n", rb->data[i]);
    }
}

int main(void)
{
    ring_buffer rb;

    memset(&rb, 0, sizeof(rb));

    printf("steps (negative to stop):\n");

    push_many(&rb);
    show(&rb);

    return 0;
}