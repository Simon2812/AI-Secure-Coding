#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *transform(const char *src)
{
    if (!src)
        return NULL;

    size_t n = strlen(src);
    char *out = (char *)malloc(n + 1);
    if (!out)
        return NULL;

    for (size_t i = 0; i < n; ++i)
    {
        out[i] = src[n - i - 1];
    }
    out[n] = '\0';

    return out;
}

void run()
{
    char *value = transform("sample");

    if (value)
    {
        printf("%s\n", value);
    }

    size_t len = value ? strlen(value) : 0;

    if (len > 0)
    {
        printf("%zu\n", len);
    }

    free(value);

    int flag = (int)len;
    if (flag < 0)
    {
        printf("never\n");
    }
}
