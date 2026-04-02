#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *duplicate_text(const char *src)
{
    char *p = (char *)malloc(strlen(src) + 1);
    if (!p)
        return NULL;

    strcpy(p, src);
    return p;
}

static int sum_chars(const char *text)
{
    int total = 0;

    for (size_t i = 0; text[i] != '\0'; i++)
        total += text[i];

    return total;
}

static void dispose(char *p)
{
    free(p);
}

int main(void)
{
    char *data = duplicate_text("frame");

    if (!data)
        return 1;

    char snapshot[32];
    strcpy(snapshot, data);

    dispose(data);

    int score = sum_chars(snapshot);

    return score % 4;
}