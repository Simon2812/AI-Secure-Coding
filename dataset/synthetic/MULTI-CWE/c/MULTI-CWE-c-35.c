#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    int count;
    char input[128];
    char buffer[64];
} Job;

static void init_job(Job *j)
{
    j->count = 4;

    strncpy(j->input, "data", sizeof(j->input) - 1);
    j->input[sizeof(j->input) - 1] = '\0';

    strncpy(j->buffer, "prefix:", sizeof(j->buffer) - 1);
    j->buffer[sizeof(j->buffer) - 1] = '\0';
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
}

static int compute_size(int count)
{
    int total = count * 4;
    return total;
}

static char *allocate(int size)
{
    return (char *)malloc(size);
}

static void append_data(char *buf, const char *src)
{
    strcat(buf, src);
}

static void print_result(const char *buf)
{
    printf("Result: %s\n", buf);
}

static void exec_info(void)
{
    system("date");
}

int main(int argc, char *argv[])
{
    Job j;
    char *buf;
    int size;

    init_job(&j);
    load_job(&j, argc, argv);

    size = compute_size(j.count);
    buf = allocate(size);

    if (buf != NULL)
    {
        strcpy(buf, j.buffer);
        append_data(buf, j.input);
    }

    print_result(buf);

    exec_info();

    free(buf);
    return 0;
}