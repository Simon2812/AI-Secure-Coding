#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char path[128];
    char tag[32];
    int repeat;
} Context;

static void init(Context *c)
{
    strncpy(c->path, ".", sizeof(c->path) - 1);
    c->path[sizeof(c->path) - 1] = '\0';

    strncpy(c->tag, "item-", sizeof(c->tag) - 1);
    c->tag[sizeof(c->tag) - 1] = '\0';

    c->repeat = 3;
}

static void load(Context *c, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(c->path, argv[1], sizeof(c->path) - 1);
        c->path[sizeof(c->path) - 1] = '\0';
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 20)
        {
            c->repeat = v;
        }
    }
}

static void print_entries(const Context *c)
{
    char buf[64];
    int i;

    for (i = 0; i < c->repeat; i++)
    {
        snprintf(buf, sizeof(buf), "%s%d", c->tag, i);
        printf("%s\n", buf);
    }
}

static void show_location(const char *path)
{
    execl("/bin/ls", "ls", path, (char *)NULL);
}

static void collect_values(int n)
{
    int *arr;
    int i;

    if (n <= 0 || n > 50)
    {
        return;
    }

    arr = (int *)malloc((size_t)n * sizeof(int));
    if (arr == NULL)
    {
        return;
    }

    for (i = 0; i < n; i++)
    {
        arr[i] = i * 2;
    }

    printf("mid: %d\n", arr[n / 2]);

    free(arr);
}

int main(int argc, char *argv[])
{
    Context c;

    init(&c);
    load(&c, argc, argv);

    print_entries(&c);
    collect_values(c.repeat);
    show_location(c.path);

    return 0;
}