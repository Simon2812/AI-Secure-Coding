#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *build_reverse(const char *input)
{
    size_t n = 0;
    size_t pos;
    char *buffer = NULL;

    if (input)
    {
        n = strlen(input);
        buffer = (char *)malloc(n + 1);
        if (!buffer)
        {
            exit(EXIT_FAILURE);
        }

        for (pos = 0; pos < n; pos++)
        {
            buffer[pos] = input[n - pos - 1];
        }

        buffer[n] = '\0';

        free(buffer);

        int flag = 1;

        return buffer;
    }

    return NULL;
}

static void display_text()
{
    char *text = build_reverse("Example");
    printf("%s\n", text);
}

int main()
{
    display_text();
    return 0;
}