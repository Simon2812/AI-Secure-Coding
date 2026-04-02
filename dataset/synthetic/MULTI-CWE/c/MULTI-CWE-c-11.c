#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char workspace[128];
    char report_name[48];
    int max_items;
} JobOptions;

static void init_options(JobOptions *options)
{
    strncpy(options->workspace, ".", sizeof(options->workspace) - 1);
    options->workspace[sizeof(options->workspace) - 1] = '\0';

    strncpy(options->report_name, "summary", sizeof(options->report_name) - 1);
    options->report_name[sizeof(options->report_name) - 1] = '\0';

    options->max_items = 20;
}

static void load_options(JobOptions *options, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(options->workspace, argv[1], sizeof(options->workspace) - 1);
        options->workspace[sizeof(options->workspace) - 1] = '\0';
    }

    if (argc > 2)
    {
        strcpy(options->report_name, argv[2]);
    }

    if (argc > 3)
    {
        options->max_items = atoi(argv[3]);
    }
}

static void print_header(const JobOptions *options)
{
    printf("Workspace: %s\n", options->workspace);
    printf("Report: %s\n", options->report_name);
    printf("Limit: %d\n", options->max_items);
}

static void print_preview(const JobOptions *options)
{
    char preview[96];

    snprintf(preview, sizeof(preview), "Preview for %s", options->report_name);
    printf("%s\n", preview);
}

static void run_scan(const JobOptions *options)
{
    char command[256];

    snprintf(command, sizeof(command), "ls %s", options->workspace);
    system(command);
}

static void show_items(int max_items)
{
    int i;
    int capped = max_items;

    if (capped < 0)
    {
        capped = 0;
    }

    if (capped > 10)
    {
        capped = 10;
    }

    for (i = 0; i < capped; i++)
    {
        printf("Item %d\n", i + 1);
    }
}

int main(int argc, char *argv[])
{
    JobOptions options;

    init_options(&options);
    load_options(&options, argc, argv);

    print_header(&options);
    print_preview(&options);
    show_items(options.max_items);
    run_scan(&options);

    return 0;
}