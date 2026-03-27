#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char name[32];
    char directory[128];
} ReportConfig;

static void init_config(ReportConfig *cfg)
{
    strncpy(cfg->name, "daily-report", sizeof(cfg->name) - 1);
    cfg->name[sizeof(cfg->name) - 1] = '\0';

    strncpy(cfg->directory, ".", sizeof(cfg->directory) - 1);
    cfg->directory[sizeof(cfg->directory) - 1] = '\0';
}

static void update_from_args(ReportConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->directory, argv[1], sizeof(cfg->directory) - 1);
        cfg->directory[sizeof(cfg->directory) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(cfg->name, argv[2], sizeof(cfg->name) - 1);
        cfg->name[sizeof(cfg->name) - 1] = '\0';
    }
}

static void print_report(const ReportConfig *cfg)
{
    printf("=== Report ===\n");
    printf("Name: %s\n", cfg->name);
    printf("Directory: %s\n", cfg->directory);
}

static void list_directory(const char *dir)
{
    char command[256];
    snprintf(command, sizeof(command), "ls %s", dir);
    system(command);
}

int main(int argc, char *argv[])
{
    ReportConfig config;

    init_config(&config);
    update_from_args(&config, argc, argv);

    print_report(&config);

    list_directory(config.directory);

    return 0;
}