#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    char path[128];
    char suffix[32];
    int count;
} Task;

static void init_task(Task *t)
{
    strncpy(t->path, ".", sizeof(t->path) - 1);
    t->path[sizeof(t->path) - 1] = '\0';

    strncpy(t->suffix, "_out", sizeof(t->suffix) - 1);
    t->suffix[sizeof(t->suffix) - 1] = '\0';

    t->count = 4;
}

static void load_task(Task *t, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(t->path, argv[1], sizeof(t->path) - 1);
        t->path[sizeof(t->path) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(t->suffix, argv[2], sizeof(t->suffix) - 1);
        t->suffix[sizeof(t->suffix) - 1] = '\0';
    }

    if (argc > 3)
    {
        t->count = atoi(argv[3]);
    }
}

static int compute_bytes(int count)
{
    return count * (int)sizeof(long);
}

static char *build_buffer(int size)
{
    if (size <= 0)
    {
        return NULL;
    }

    return (char *)malloc((size_t)size);
}

static void append_suffix(char *buf, const char *suffix)
{
    strncat(buf, suffix, strlen(suffix));
}

static void execute_task(const char *path)
{
    char command[256];

    snprintf(command, sizeof(command), "ls -l %s", path);
    system(command);
}

int main(int argc, char *argv[])
{
    Task t;
    int bytes;
    char *buffer;

    init_task(&t);
    load_task(&t, argc, argv);

    bytes = compute_bytes(t.count);
    buffer = build_buffer(bytes);

    if (buffer != NULL)
    {
        buffer[0] = '\0';
        append_suffix(buffer, t.suffix);
        printf("Buffer: %s\n", buffer);
    }

    execute_task(t.path);

    free(buffer);
    return 0;
}