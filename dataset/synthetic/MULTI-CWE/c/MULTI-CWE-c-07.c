#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char base_dir[128];
    char user_arg[128];
} TaskConfig;

static void init_config(TaskConfig *cfg)
{
    strncpy(cfg->base_dir, ".", sizeof(cfg->base_dir) - 1);
    cfg->base_dir[sizeof(cfg->base_dir) - 1] = '\0';

    strncpy(cfg->user_arg, "", sizeof(cfg->user_arg) - 1);
    cfg->user_arg[sizeof(cfg->user_arg) - 1] = '\0';
}

static void load_input(TaskConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->user_arg, argv[1], sizeof(cfg->user_arg) - 1);
        cfg->user_arg[sizeof(cfg->user_arg) - 1] = '\0';
    }
}

static void run_default_listing(const char *dir)
{
    char command[256];
    snprintf(command, sizeof(command), "ls %s", dir);
    system(command);
}

static void run_user_listing(const char *arg)
{
    char command[256];
    snprintf(command, sizeof(command), "ls %s", arg);
    system(command);
}

static void execute(const TaskConfig *cfg)
{
    run_default_listing(cfg->base_dir);
    run_user_listing(cfg->user_arg);
}

int main(int argc, char *argv[])
{
    TaskConfig cfg;

    init_config(&cfg);
    load_input(&cfg, argc, argv);

    execute(&cfg);

    return 0;
}