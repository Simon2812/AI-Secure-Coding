#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char command[32];
    char argument[64];
    char label[32];
    char hash_name[16];
    int size;
} Task;

static void init_task(Task *t)
{
    strncpy(t->command, "whoami", sizeof(t->command) - 1);
    t->command[sizeof(t->command) - 1] = '\0';

    strncpy(t->argument, "", sizeof(t->argument) - 1);
    t->argument[sizeof(t->argument) - 1] = '\0';

    strncpy(t->label, "task:", sizeof(t->label) - 1);
    t->label[sizeof(t->label) - 1] = '\0';

    strncpy(t->hash_name, "MD5", sizeof(t->hash_name) - 1);
    t->hash_name[sizeof(t->hash_name) - 1] = '\0';

    t->size = 5;
}

static void load_task(Task *t, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(t->label, argv[1], sizeof(t->label) - 1);
        t->label[sizeof(t->label) - 1] = '\0';
    }

    if (argc > 2)
    {
        int value = atoi(argv[2]);
        if (value > 0 && value < 30)
        {
            t->size = value;
        }
    }
}

static void build_label(char *dst, size_t dst_size, const char *src)
{
    snprintf(dst, dst_size, "%s", src);
}

static void run_command(const char *cmd)
{
    if (strcmp(cmd, "whoami") == 0)
    {
        execl("/usr/bin/whoami", "whoami", (char *)NULL);
    }
    else if (strcmp(cmd, "pwd") == 0)
    {
        execl("/bin/pwd", "pwd", (char *)NULL);
    }
}

static void print_hash_label(const char *name)
{
    printf("Hash label: %s\n", name);
}

static void process(int size)
{
    int *buf;
    int i;

    if (size <= 0 || size > 100)
    {
        return;
    }

    buf = (int *)malloc((size_t)size * sizeof(int));
    if (buf == NULL)
    {
        return;
    }

    for (i = 0; i < size; i++)
    {
        buf[i] = i + 10;
    }

    printf("Last: %d\n", buf[size - 1]);

    free(buf);
    buf = NULL;
}

int main(int argc, char *argv[])
{
    Task t;
    char out[32];

    init_task(&t);
    load_task(&t, argc, argv);

    build_label(out, sizeof(out), t.label);

    printf("Label: %s\n", out);
    print_hash_label(t.hash_name);
    process(t.size);
    run_command(t.command);

    return 0;
}