#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sanitize(char *buf)
{
    for (size_t i = 0; buf[i] != '\0'; i++)
    {
        if (buf[i] == '\n')
            buf[i] = ' ';
    }
}

static void transform(char *buf)
{
    free(buf);
}

static int evaluate(const char *buf)
{
    int score = 0;

    for (size_t i = 0; buf[i] != '\0'; i++)
        score += buf[i];

    return score;
}

int main(void)
{
    char *input = (char *)malloc(32);
    if (!input)
        return 1;

    strcpy(input, "example");

    sanitize(input);

    char *alias = input;

    transform(input);

    evaluate(alias);

    return 0;
}