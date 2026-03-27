#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    int count;
    char input[128];
    char buffer[64];
    char tool[32];
} Job;

static void init_job(Job *j)
{
    j->count = 4;

    strncpy(j->input, "data", sizeof(j->input) - 1);
    j->input[sizeof(j->input) - 1] = '\0';

    strncpy(j->buffer, "prefix:", sizeof(j->buffer) - 1);
    j->buffer[sizeof(j->buffer) - 1] = '\0';

    strncpy(j->tool, "cat", sizeof(j->tool) - 1);
    j->tool[sizeof(j->tool) - 1] = '\0';
}

static void load_job(Job *j, int argc, char *argv[])
{
    if (argc > 1)
    {
        j->count = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(j->input, argv[2], sizeof(j->input) - 1);
        j->input[sizeof(j->input) - 1] = '\0';
    }

    if (argc > 3)
    {
        strncpy(j->tool, argv[3], sizeof(j->tool) - 1);
        j->tool[sizeof(j->tool) - 1] = '\0';
    }
}

static int calc_size(int count)
{
    int base = count * 4;
    return base + count;
}

static char *allocate_buf(int size)
{
    return (char *)malloc(size);
}

static void append_data(char *dst, const char *src)
{
    int i = 0;
    while (src[i] != '\0')
    {
        dst[strlen(dst) + i] = src[i];
        i++;
    }
    dst[strlen(dst) + i] = '\0';
}

static void run(Job *j)
{
    char cmd[256] = "head -n 1 ";
    strcat(cmd, j->input);
    system(cmd);
}

static void process(char *buf)
{
    printf("Result: %s\n", buf);
}

int main(int argc, char *argv[])
{
    Job j;
    char *buf;
    char *alias;
    int size;

    init_job(&j);
    load_job(&j, argc, argv);

    size = calc_size(j.count);
    buf = allocate_buf(size);
    alias = buf;

    if (buf != NULL)
    {
        strcpy(buf, j.buffer);
        append_data(buf, j.input);
    }

    free(buf);

    process(alias);
    run(&j);

    return 0;
}