#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned short width;
    unsigned short height;
    unsigned char pixels[24];
} icon_frame;

static int read_header(FILE *fp, unsigned short *w, unsigned short *h)
{
    char line[64];
    char *sep;

    if (fgets(line, sizeof(line), fp) == NULL)
    {
        return 0;
    }

    sep = strchr(line, 'x');
    if (sep == NULL)
    {
        return 0;
    }

    *sep = '\0';
    *w = (unsigned short)atoi(line);
    *h = (unsigned short)atoi(sep + 1);
    return 1;
}

static void load_pixels(FILE *fp, icon_frame *frame)
{
    char line[256];
    int need;
    int i = 0;
    char *part;

    need = frame->width * frame->height;

    if (fgets(line, sizeof(line), fp) == NULL)
    {
        return;
    }

    part = strtok(line, ",");

    while (part != NULL && i < need)
    {
        frame->pixels[i] = (unsigned char)atoi(part);
        i++;
        part = strtok(NULL, ",");
    }
}

static void print_frame(const icon_frame *frame)
{
    int i;

    printf("%u x %u\n", frame->width, frame->height);
    for (i = 0; i < 24; i++)
    {
        printf("%u\n", frame->pixels[i]);
    }
}

int main(int argc, char **argv)
{
    FILE *fp;
    icon_frame frame;

    memset(&frame, 0, sizeof(frame));

    if (argc != 2)
    {
        fprintf(stderr, "usage: %s file\n", argv[0]);
        return 1;
    }

    fp = fopen(argv[1], "r");
    if (fp == NULL)
    {
        return 1;
    }

    if (read_header(fp, &frame.width, &frame.height))
    {
        load_pixels(fp, &frame);
        print_frame(&frame);
    }

    fclose(fp);
    return 0;
}