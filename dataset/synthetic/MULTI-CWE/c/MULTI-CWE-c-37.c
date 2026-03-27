#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char filename[128];
    char prefix[32];
    char crypto_label[16];
    int count;
} Config;

static void init_config(Config *cfg)
{
    strncpy(cfg->filename, "log.txt", sizeof(cfg->filename) - 1);
    cfg->filename[sizeof(cfg->filename) - 1] = '\0';

    strncpy(cfg->prefix, "entry:", sizeof(cfg->prefix) - 1);
    cfg->prefix[sizeof(cfg->prefix) - 1] = '\0';

    strncpy(cfg->crypto_label, "SHA1", sizeof(cfg->crypto_label) - 1);
    cfg->crypto_label[sizeof(cfg->crypto_label) - 1] = '\0';

    cfg->count = 3;
}

static void load_config(Config *cfg, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(cfg->filename, argv[1], sizeof(cfg->filename) - 1);
        cfg->filename[sizeof(cfg->filename) - 1] = '\0';
    }

    if (argc > 2)
    {
        int value = atoi(argv[2]);
        if (value > 0 && value < 20)
        {
            cfg->count = value;
        }
    }
}

static void build_entry(char *dst, size_t dst_size, const char *prefix, const char *name)
{
    snprintf(dst, dst_size, "%s%s", prefix, name);
}

static void write_file(const char *filename, const char *content)
{
    FILE *f = fopen(filename, "w");
    if (f == NULL)
    {
        return;
    }

    fprintf(f, "%s\n", content);
    fclose(f);
}

static void execute_info(void)
{
    execl("/bin/pwd", "pwd", (char *)NULL);
}

static void print_crypto(const char *label)
{
    printf("Crypto label: %s\n", label);
}

static void process_data(int count)
{
    int *arr;
    int i;

    if (count <= 0 || count > 50)
    {
        return;
    }

    arr = (int *)malloc((size_t)count * sizeof(int));
    if (arr == NULL)
    {
        return;
    }

    for (i = 0; i < count; i++)
    {
        arr[i] = i;
    }

    printf("First: %d\n", arr[0]);

    free(arr);
}

int main(int argc, char *argv[])
{
    Config cfg;
    char entry[64];

    init_config(&cfg);
    load_config(&cfg, argc, argv);

    build_entry(entry, sizeof(entry), cfg.prefix, cfg.filename);

    write_file(cfg.filename, entry);
    print_crypto(cfg.crypto_label);
    process_data(cfg.count);
    execute_info();

    return 0;
}