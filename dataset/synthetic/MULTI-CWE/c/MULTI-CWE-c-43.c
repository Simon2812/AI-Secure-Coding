#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char source[128];
    char mode[16];
    int limit;
} Config;

typedef struct
{
    int value;
    char label[32];
} Item;

static void init(Config *cfg)
{
    snprintf(cfg->source, sizeof(cfg->source), "%s", "input.dat");
    snprintf(cfg->mode, sizeof(cfg->mode), "%s", "scan");
    cfg->limit = 6;
}

static void parse(Config *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        snprintf(cfg->source, sizeof(cfg->source), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int v = atoi(argv[2]);
        if (v > 0 && v < 100)
        {
            cfg->limit = v;
        }
    }

    if (argc > 3)
    {
        snprintf(cfg->mode, sizeof(cfg->mode), "%s", argv[3]);
    }
}

static int fill_items(Item *items, int max, const char *seed)
{
    int i;
    size_t base = strlen(seed);

    for (i = 0; i < max; i++)
    {
        items[i].value = (int)(base + i);

        snprintf(items[i].label, sizeof(items[i].label),
                 "%s_%d", seed, i);
    }

    return max;
}

static void summarize(const Item *items, int n)
{
    int i;
    int total = 0;

    for (i = 0; i < n; i++)
    {
        total += items[i].value;
    }

    if (n > 0)
    {
        printf("sum=%d\n", total);
    }
}

static void execute_mode(const char *mode, const char *src)
{
    if (strcmp(mode, "scan") == 0)
    {
        execl("/usr/bin/stat", "stat", src, (char *)NULL);
    }
    else if (strcmp(mode, "list") == 0)
    {
        execl("/bin/ls", "ls", "-a", src, (char *)NULL);
    }
}

int main(int argc, char *argv[])
{
    Config cfg;
    Item *items;
    int count;

    init(&cfg);
    parse(&cfg, argc, argv);

    if (cfg.limit <= 0 || cfg.limit > 200)
    {
        return 0;
    }

    items = (Item *)malloc((size_t)cfg.limit * sizeof(Item));
    if (items == NULL)
    {
        return 0;
    }

    count = fill_items(items, cfg.limit, cfg.source);

    summarize(items, count);

    free(items);

    execute_mode(cfg.mode, cfg.source);

    return 0;
}