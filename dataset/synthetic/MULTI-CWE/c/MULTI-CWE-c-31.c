#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char path[128];
    char name[32];
    int limit;
} Task;

static void init_task(Task *t)
{
    strncpy(t->path, ".", sizeof(t->path) - 1);
    t->path[sizeof(t->path) - 1] = '\0';

    strncpy(t->name, "job", sizeof(t->name) - 1);
    t->name[sizeof(t->name) - 1] = '\0';

    t->limit = 5;
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
        int i = 0;
        while (argv[2][i] != '\0')
        {
            t->name[i] = argv[2][i];
            i++;
        }
        t->name[i] = '\0';
    }

    if (argc > 3)
    {
        t->limit = atoi(argv[3]);
    }
}

static void safe_list(void)
{
    system("pwd");
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
    Task t;

    init_task(&t);
    load_task(&t, argc, argv);

    safe_list();
    print_items(t.limit);

    printf("Name: %s\n", t.name);

    return 0;
}