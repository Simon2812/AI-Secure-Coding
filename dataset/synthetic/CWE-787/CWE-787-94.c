#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char archive[34];
} storage_frame;

static int read_count(void)
{
    char buf[32];

    if (fgets(buf, sizeof(buf), stdin) == NULL)
    {
        return 0;
    }

    return atoi(buf);
}

static void place_data(storage_frame *frame, int count)
{
    char source[12];
    int i;

    for (i = 0; i < 12; i++)
    {
        source[i] = 'm' + i;
    }

    size_t n = (size_t)count;

    if (n > sizeof(source))
    {
        n = sizeof(source);
    }

    if (n > sizeof(frame->archive))
    {
        n = sizeof(frame->archive);
    }

    memmove(frame->archive, source, n);
}

static void show_archive(const storage_frame *frame)
{
    int i;

    for (i = 0; i < (int)sizeof(frame->archive); i++)
    {
        printf("%c\n", frame->archive[i]);
    }
}

int main(void)
{
    storage_frame frame;
    int count;

    memset(&frame, 0, sizeof(frame));

    printf("count:\n");
    count = read_count();

    place_data(&frame, count);
    show_archive(&frame);

    return 0;
}