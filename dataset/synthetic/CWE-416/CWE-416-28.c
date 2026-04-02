#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *token;
} ParserState;

static ParserState *init_state(const char *text)
{
    ParserState *s = (ParserState *)malloc(sizeof(ParserState));
    if (!s)
        return NULL;

    s->token = (char *)malloc(strlen(text) + 1);
    if (!s->token)
    {
        free(s);
        return NULL;
    }

    strcpy(s->token, text);
    return s;
}

static void discard_token(ParserState *s)
{
    if (s && s->token)
        free(s->token);
}

static int token_metric(const char *t)
{
    int v = 0;

    for (size_t i = 0; t[i] != '\0'; i++)
        v += t[i];

    return v;
}

int main(void)
{
    ParserState *state = init_state("header");
    if (!state)
        return 1;

    const char *view = state->token;

    discard_token(state);

    int result = token_metric(view);

    printf("%d\n", result);

    free(state);

    return 0;
}