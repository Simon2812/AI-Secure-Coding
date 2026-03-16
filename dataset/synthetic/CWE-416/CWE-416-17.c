#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    int length;
} Buffer;

static void fill(Buffer *b)
{
    for (int i = 0; i < b->length; i++)
        b->data[i] = (char)(i + 65);
}

static void release(Buffer *b)
{
    if (b->data)
        free(b->data);
}

static int analyze(Buffer *b)
{
    int sum = 0;

    for (int i = 0; i < b->length; i++)
        sum += b->data[i];

    return sum;
}

int main(void)
{
    Buffer buf;
    buf.length = 8;
    buf.data = malloc(buf.length);

    if (!buf.data)
        return 1;

    fill(&buf);

    Buffer *shadow = &buf;

    release(&buf);

    int res = analyze(shadow);

    printf("%d\n", res);

    return 0;
}