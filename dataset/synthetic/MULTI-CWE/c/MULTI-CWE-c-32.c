#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int count;
    char path[128];
    char name[32];
} Config;

static void init_config(Config *cfg)
{
    cfg->count = 4;

    strncpy(cfg->path, ".", sizeof(cfg->path) - 1);
    cfg->path[sizeof(cfg->path) - 1] = '\0';

    strncpy(cfg->name, "task", sizeof(cfg->name) - 1);
    cfg->name[sizeof(cfg->name) - 1] = '\0';
}

static void load_config(Config *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        cfg->count = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(cfg->path, argv[2], sizeof(cfg->path) - 1);
        cfg->path[sizeof(cfg->path) - 1] = '\0';
    }

    if (argc > 3)
    {
        strncpy(cfg->name, argv[3], sizeof(cfg->name) - 1);
        cfg->name[sizeof(cfg->name) - 1] = '\0';
    }
}

static int compute(int count)
{
    return count + 10;
}

static char *create_copy(const char *src)
{
    char *dst = (char *)malloc(strlen(src) + 1);

    if (dst == NULL)
    {
        return NULL;
    }

    strcpy(dst, src);
    return dst;
}

static void cleanup(char *ptr)
{
    if (ptr != NULL)
    {
        free(ptr);
    }
}

static void safe_exec(void)
{
    system("whoami");
}

int main(int argc, char *argv[])
{
    Config cfg;
    char *copy;

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    copy = create_copy(cfg.name);

    printf("Copy: %s\n", copy);

    cleanup(copy);

    safe_exec();

    return 0;
}