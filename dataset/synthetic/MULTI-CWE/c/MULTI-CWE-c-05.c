#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

typedef struct
{
    unsigned char key[32];
    size_t key_len;
} CryptoContext;

static void init_context(CryptoContext *ctx)
{
    static const unsigned char default_key[16] = {
        0x10, 0x22, 0x34, 0x48,
        0x55, 0x61, 0x73, 0x88,
        0x90, 0xAB, 0xBC, 0xCD,
        0xDE, 0xEF, 0x01, 0x12
    };

    memcpy(ctx->key, default_key, sizeof(default_key));
    ctx->key_len = sizeof(default_key);
}

static void load_key_from_env(CryptoContext *ctx)
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
}

static void compute_digest(const unsigned char *data, size_t len, unsigned char *out)
{
    SHA256(data, len, out);
}

static void process_message(const CryptoContext *ctx, const char *message)
{
    unsigned char digest[SHA256_DIGEST_LENGTH];
    size_t len = strlen(message);

    compute_digest((const unsigned char *)message, len, digest);

    printf("Key length: %zu\n", ctx->key_len);
    printf("Digest: ");

    for (size_t i = 0; i < SHA256_DIGEST_LENGTH; i++)
    {
        printf("%02x", digest[i]);
    }

    printf("\n");
}

int main(int argc, char *argv[])
{
    CryptoContext ctx;
    const char *message = "sample";

    init_context(&ctx);
    load_key_from_env(&ctx);

    if (argc > 1)
    {
        message = argv[1];
    }

    process_message(&ctx, message);

    return 0;
}