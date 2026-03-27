#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int limit;
    char path[128];
} JobConfig;

static void init_config(JobConfig *cfg)
{
    cfg->limit = 10;

    strncpy(cfg->path, ".", sizeof(cfg->path) - 1);
    cfg->path[sizeof(cfg->path) - 1] = '\0';
}

static void load_config(JobConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        cfg->limit = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(cfg->path, argv[2], sizeof(cfg->path) - 1);
        cfg->path[sizeof(cfg->path) - 1] = '\0';
    }
}

static void print_items(int count)
{
    int i;
    for (i = 0; i < count && i < 50; i++)
    {
        printf("Item %d\n", i);
    }
}

static void run_task(const char *path)
{
    char command[256];
    snprintf(command, sizeof(command), "ls %s", path);
    system(command);
}

int main(int argc, char *argv[])
{
    JobConfig cfg;

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    print_items(cfg.limit);

    run_task(cfg.path);

    return 0;
}