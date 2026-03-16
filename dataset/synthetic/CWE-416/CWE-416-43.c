#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
    int size;
} Slice;

static int init_slice(Slice *s, const char *src)
{
    s->size = (int)strlen(src);
    s->text = (char *)malloc((size_t)s->size + 1);
    if (!s->text)
        return 0;

    memcpy(s->text, src, (size_t)s->size + 1);
    return 1;
}

static int fold_slice(const Slice *s)
{
    int total = 0;

    for (int i = 0; i < s->size; ++i)
        total += s->text[i];

    return total;
}

int main(void)
{
    Slice part;
    if (!init_slice(&part, "header_block"))
        return 1;

    char mirror[64];
    memcpy(mirror, part.text, (size_t)part.size + 1);

    free(part.text);

    int score = 0;
    for (int i = 0; mirror[i] != '\0'; ++i)
        score += mirror[i];

    printf("%d\n", score);

    if (score < 0)
        puts("skip");

    return 0;
}