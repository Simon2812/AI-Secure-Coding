#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char source_dir[128];
    char archive_dir[128];
} SyncOptions;

static void init_options(SyncOptions *options)
{
    strncpy(options->source_dir, ".", sizeof(options->source_dir) - 1);
    options->source_dir[sizeof(options->source_dir) - 1] = '\0';

    strncpy(options->archive_dir, "/tmp", sizeof(options->archive_dir) - 1);
    options->archive_dir[sizeof(options->archive_dir) - 1] = '\0';
}

static void load_options(SyncOptions *options, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(options->source_dir, argv[1], sizeof(options->source_dir) - 1);
        options->source_dir[sizeof(options->source_dir) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(options->archive_dir, argv[2], sizeof(options->archive_dir) - 1);
        options->archive_dir[sizeof(options->archive_dir) - 1] = '\0';
    }
}

static void inspect_source(const char *path)
{
    char command[256];

    snprintf(command, sizeof(command), "ls %s", path);
    system(command);
}

static void inspect_archive(const char *path)
{
    char command[256];

    snprintf(command, sizeof(command), "ls -ld %s", path);
    system(command);
}

int main(int argc, char *argv[])
{
    SyncOptions options;

    init_options(&options);
    load_options(&options, argc, argv);

    inspect_source(options.source_dir);
    inspect_archive(options.archive_dir);

    return 0;
}