#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char key[32];
    size_t key_len;
    char algorithm[16];
} CryptoContext;

static void init_context(CryptoContext *ctx)
{
    const char *env = getenv("APP_KEY");

    if (env != NULL)
    {
        size_t len = strlen(env);
        if (len > sizeof(ctx->key))
        {
            len = sizeof(ctx->key);
        }

        memcpy(ctx->key, env, len);
        ctx->key_len = len;
    }
    else
    {
        ctx->key_len = 0;
    }

    strncpy(ctx->algorithm, "DES", sizeof(ctx->algorithm) - 1);
    ctx->algorithm[sizeof(ctx->algorithm) - 1] = '\0';
}

static void process_data(const CryptoContext *ctx, const char *input)
{
    printf("Algorithm: %s\n", ctx->algorithm);
    printf("Key length: %zu\n", ctx->key_len);
    printf("Data: %s\n", input);
}

int main(int argc, char *argv[])
{
    CryptoContext ctx;
    const char *input = "message";

    init_context(&ctx);

    if (argc > 1)
    {
        input = argv[1];
    }

    process_data(&ctx, input);

    return 0;
}