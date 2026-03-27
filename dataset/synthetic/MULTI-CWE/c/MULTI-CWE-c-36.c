#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char command_name[32];
    char command_arg[64];
    char title[32];
    char algorithm[16];
    char digest_name[16];
    int count;
} ReportConfig;

static void init_config(ReportConfig *cfg)
{
    strncpy(cfg->command_name, "date", sizeof(cfg->command_name) - 1);
    cfg->command_name[sizeof(cfg->command_name) - 1] = '\0';

    strncpy(cfg->command_arg, "", sizeof(cfg->command_arg) - 1);
    cfg->command_arg[sizeof(cfg->command_arg) - 1] = '\0';

    strncpy(cfg->title, "daily-report", sizeof(cfg->title) - 1);
    cfg->title[sizeof(cfg->title) - 1] = '\0';

    strncpy(cfg->algorithm, "RC4", sizeof(cfg->algorithm) - 1);
    cfg->algorithm[sizeof(cfg->algorithm) - 1] = '\0';

    strncpy(cfg->digest_name, "MD5", sizeof(cfg->digest_name) - 1);
    cfg->digest_name[sizeof(cfg->digest_name) - 1] = '\0';

    cfg->count = 4;
}

static void load_config(ReportConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->title, argv[1], sizeof(cfg->title) - 1);
        cfg->title[sizeof(cfg->title) - 1] = '\0';
    }

    if (argc > 2)
    {
        int value = atoi(argv[2]);
        if (value > 0 && value < 50)
        {
            cfg->count = value;
        }
    }
}

static void build_title(char *dst, size_t dst_size, const char *src)
{
    snprintf(dst, dst_size, "%s", src);
}

static void run_command(const char *name, const char *arg)
{
    if (strcmp(name, "date") == 0)
    {
        execl("/bin/date", "date", (char *)NULL);
    }
    else if (strcmp(name, "pwd") == 0)
    {
        execl("/bin/pwd", "pwd", (char *)NULL);
    }
    else if (strcmp(name, "whoami") == 0)
    {
        execl("/usr/bin/whoami", "whoami", (char *)NULL);
    }
    else if (strcmp(name, "echo") == 0)
    {
        execl("/bin/echo", "echo", arg, (char *)NULL);
    }
}

static void print_crypto_labels(const ReportConfig *cfg)
{
    printf("Algorithm label: %s\n", cfg->algorithm);
    printf("Digest label: %s\n", cfg->digest_name);
}

static void process_items(int count)
{
    int *items;
    int i;

    if (count <= 0 || count > 100)
    {
        return;
    }

    items = (int *)malloc((size_t)count * sizeof(int));
    if (items == NULL)
    {
        return;
    }

    for (i = 0; i < count; i++)
    {
        items[i] = i + 1;
    }

    printf("Last item: %d\n", items[count - 1]);

    free(items);
    items = NULL;
}

int main(int argc, char *argv[])
{
    ReportConfig cfg;
    char display_title[32];

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    build_title(display_title, sizeof(display_title), cfg.title);

    printf("Title: %s\n", display_title);
    print_crypto_labels(&cfg);
    process_items(cfg.count);
    run_command(cfg.command_name, cfg.command_arg);

    return 0;
}