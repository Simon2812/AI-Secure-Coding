#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *context;
} Callback;

static void run_callback(Callback *cb)
{
    if (!cb || !cb->context)
        return;

    int score = 0;
    for (size_t i = 0; cb->context[i] != '\0'; i++)
        score += cb->context[i];

    printf("%d\n", score);
}

static void register_callback(Callback *cb, char *ctx)
{
    cb->context = ctx;
}

static void clear_context(char *ctx)
{
    free(ctx);
}

int main(void)
{
    Callback cb;

    char *buffer = (char *)malloc(32);
    if (!buffer)
        return 1;

    strcpy(buffer, "event_payload");

    register_callback(&cb, buffer);

    clear_context(buffer);

    run_callback(&cb);

    return 0;
}