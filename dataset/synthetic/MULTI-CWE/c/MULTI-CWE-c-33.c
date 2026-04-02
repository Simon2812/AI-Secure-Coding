#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char input[128];
    char buffer[64];
    int limit;
} Job;

static void init_job(Job *j)
{
    strncpy(j->input, ".", sizeof(j->input) - 1);
    j->input[sizeof(j->input) - 1] = '\0';

    strncpy(j->buffer, "start:", sizeof(j->buffer) - 1);
    j->buffer[sizeof(j->buffer) - 1] = '\0';

    j->limit = 5;
}

static void load_job(Job *j, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(j->input, argv[1], sizeof(j->input) - 1);
        j->input[sizeof(j->input) - 1] = '\0';
    }

    if (argc > 2)
    {
        strcat(j->buffer, argv[2]);
    }

    if (argc > 3)
    {
        j->limit = atoi(argv[3]);
    }
}

static void run(const char *input)
{
    char cmd[256] = "wc -l ";
    strcat(cmd, input);
    system(cmd);
}

static void safe_memory_usage(void)
{
    char *tmp = (char *)malloc(32);

    if (tmp != NULL)
    {
        strcpy(tmp, "ok");
        printf("%s\n", tmp);
        free(tmp);  // safe usage
    }
}

static void print_items(int limit)
{
    int i;
    int count = limit;

    if (count < 0)
    {
        count = 0;
    }

    if (count > 10)
    {
        count = 10;
    }

    for (i = 0; i < count; i++)
    {
        printf("Item %d\n", i + 1);
    }
}

int main(int argc, char *argv[])
{
    Job j;

    init_job(&j);
    load_job(&j, argc, argv);

    printf("Buffer: %s\n", j.buffer);

    safe_memory_usage();   // SAFE CWE-416 pattern
    print_items(j.limit);
    run(j.input);

    return 0;
}