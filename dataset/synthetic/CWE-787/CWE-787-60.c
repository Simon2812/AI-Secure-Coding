#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char data[36];
} frame;

static int read_stride(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 1;
    }

    return atoi(buf);
}

static void scatter_pattern(frame *f, int stride)
{
    char pattern[6];
    int pos = 0;
    int i;

    for (i = 0; i < 6; i++)
    {
        pattern[i] = 'k' + i;
    }

    for (i = 0; i < 10; i++)
    {
        f->data[pos] = pattern[i % 6];
        pos += stride;
    }
}

static void show_frame(const frame *f)
{
    int i;

    for (i = 0; i < 36; i++)
    {
        printf("%c\n", f->data[i]);
    }
}

int main(void)
{
    frame f;
    int stride;

    memset(&f, 0, sizeof(f));

    printf("stride:\n");
    stride = read_stride();

    scatter_pattern(&f, stride);
    show_frame(&f);

    return 0;
}