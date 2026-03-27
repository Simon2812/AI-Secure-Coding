#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char path[128];
    char tag[32];
    int limit;
} ExportConfig;

static void init_config(ExportConfig *cfg)
{
    strncpy(cfg->path, ".", sizeof(cfg->path) - 1);
    cfg->path[sizeof(cfg->path) - 1] = '\0';

    strncpy(cfg->tag, "export", sizeof(cfg->tag) - 1);
    cfg->tag[sizeof(cfg->tag) - 1] = '\0';

    cfg->limit = 5;
}

static void load_config(ExportConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->path, argv[1], sizeof(cfg->path) - 1);
        cfg->path[sizeof(cfg->path) - 1] = '\0';
    }

    if (argc > 2)
    {
        strcat(cfg->tag, argv[2]);
    }

    if (argc > 3)
    {
        cfg->limit = atoi(argv[3]);
    }
}

static void run_export(const char *path)
{
    char *args[3];

    args[0] = "ls";
    args[1] = (char *)path;
    args[2] = NULL;

    execvp("ls", args);
}

static void print_preview(int limit)
{
    int i;
    int count = limit;

    if (count < 0)
    {
        count = 0;
    }

    if (count > 6)
    {
        count = 6;
    }

    for (i = 0; i < count; i++)
    {
        printf("Item %d\n", i + 1);
    }
}

int main(int argc, char *argv[])
{
    ExportConfig cfg;

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    print_preview(cfg.limit);
    run_export(cfg.path);

    return 0;
}