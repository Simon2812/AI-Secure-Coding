#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char key[32];
    char algorithm[16];
} CryptoConfig;

static void init_config(CryptoConfig *cfg)
{
    strncpy(cfg->key, "ABCD1234SECRETKEY", sizeof(cfg->key) - 1);
    cfg->key[sizeof(cfg->key) - 1] = '\0';

    strncpy(cfg->algorithm, "DES", sizeof(cfg->algorithm) - 1);
    cfg->algorithm[sizeof(cfg->algorithm) - 1] = '\0';
}

static void load_key(CryptoConfig *cfg)
{
    const char *env = getenv("APP_KEY");

    if (env != NULL)
    {
        size_t len = strlen(env);
        if (len < sizeof(cfg->key))
        {
            memcpy(cfg->key, env, len);
            cfg->key[len] = '\0';
        }
    }
}

static void process(const CryptoConfig *cfg, const char *input)
{
    printf("Algorithm: %s\n", cfg->algorithm);
    printf("Key length: %zu\n", strlen(cfg->key));
    printf("Input: %s\n", input);
}

int main(int argc, char *argv[])
{
    CryptoConfig cfg;
    const char *input = "data";

    init_config(&cfg);
    load_key(&cfg);

    if (argc > 1)
    {
        input = argv[1];
    }

    process(&cfg, input);

    return 0;
}