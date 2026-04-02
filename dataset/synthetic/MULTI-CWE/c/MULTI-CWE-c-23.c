#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char command_line[128];
    char label[24];
    char note[96];
} MonitorConfig;

typedef struct
{
    char text[96];
    size_t length;
} Entry;

static void init_config(MonitorConfig *cfg)
{
    strncpy(cfg->command_line, "ls .", sizeof(cfg->command_line) - 1);
    cfg->command_line[sizeof(cfg->command_line) - 1] = '\0';

    strncpy(cfg->label, "daily", sizeof(cfg->label) - 1);
    cfg->label[sizeof(cfg->label) - 1] = '\0';

    strncpy(cfg->note, "ready", sizeof(cfg->note) - 1);
    cfg->note[sizeof(cfg->note) - 1] = '\0';
}

static void load_config(MonitorConfig *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->command_line, argv[1], sizeof(cfg->command_line) - 1);
        cfg->command_line[sizeof(cfg->command_line) - 1] = '\0';
    }

    if (argc > 2)
    {
        sscanf(argv[2], "%s", cfg->label);
    }

    if (argc > 3)
    {
        strncpy(cfg->note, argv[3], sizeof(cfg->note) - 1);
        cfg->note[sizeof(cfg->note) - 1] = '\0';
    }
}

static Entry *create_entry(const char *note)
{
    Entry *entry = (Entry *)malloc(sizeof(Entry));
    if (entry == NULL)
    {
        return NULL;
    }

    strncpy(entry->text, note, sizeof(entry->text) - 1);
    entry->text[sizeof(entry->text) - 1] = '\0';
    entry->length = strlen(entry->text);
    return entry;
}

static void print_entry(const Entry *entry)
{
    if (entry != NULL)
    {
        printf("Entry: %s (%zu)\n", entry->text, entry->length);
    }
}

static void release_entry(Entry *entry)
{
    if (entry != NULL)
    {
        free(entry);
    }
}

static void run_capture(const char *command_line)
{
    char line[128];
    FILE *stream = popen(command_line, "r");

    if (stream == NULL)
    {
        return;
    }

    if (fgets(line, sizeof(line), stream) != NULL)
    {
        printf("Output: %s", line);
    }

    pclose(stream);
}

static void print_summary(const MonitorConfig *cfg)
{
    printf("Label: %s\n", cfg->label);
    printf("Command: %s\n", cfg->command_line);
    printf("Note: %s\n", cfg->note);
}

int main(int argc, char *argv[])
{
    MonitorConfig cfg;
    Entry *entry;

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    print_summary(&cfg);

    entry = create_entry(cfg.note);
    release_entry(entry);
    print_entry(entry);

    run_capture(cfg.command_line);

    return 0;
}