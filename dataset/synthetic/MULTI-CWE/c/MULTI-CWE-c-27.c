#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    int index;
    char name[40];
    char extra[64];
} BatchConfig;

static void init_config(BatchConfig *cfg)
{
    cfg->index = 2;

    strncpy(cfg->name, "records", sizeof(cfg->name) - 1);
    cfg->name[sizeof(cfg->name) - 1] = '\0';

    strncpy(cfg->extra, "suffix", sizeof(cfg->extra) - 1);
    cfg->extra[sizeof(cfg->extra) - 1] = '\0';
}

static void load_config(BatchConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        cfg->index = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(cfg->name, argv[2], sizeof(cfg->name) - 1);
        cfg->name[sizeof(cfg->name) - 1] = '\0';
    }

    if (argc > 3)
    {
        strncpy(cfg->extra, argv[3], sizeof(cfg->extra) - 1);
        cfg->extra[sizeof(cfg->extra) - 1] = '\0';
    }
}

static int calculate_offset(int index)
{
    return index + 1000000000;
}

static char *create_text(const char *name)
{
    char *text = (char *)malloc(64);

    if (text == NULL)
    {
        return NULL;
    }

    strcpy(text, name);
    return text;
}

static void append_extra(char *text, const char *extra)
{
    int len = strlen(text);
    int i = 0;

    while (extra[i] != '\0')
    {
        text[len + i] = extra[i];
        i++;
    }

    text[len + i] = '\0';
}

static void process_text(char *text)
{
    printf("Text: %s\n", text);
}

int main(int argc, char *argv[])
{
    BatchConfig cfg;
    char *text;
    char *alias;
    int offset;

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    offset = calculate_offset(cfg.index);

    text = create_text(cfg.name);
    alias = text;

    append_extra(text, cfg.extra);

    free(text);

    process_text(alias);

    return 0;
}