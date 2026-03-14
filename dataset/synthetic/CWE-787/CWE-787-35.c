#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_count(const char *text)
{
    if (text == NULL)
    {
        return 0;
    }
    return atoi(text);
}

static void copy_values(int *dst, const int *src, int count)
{
    memcpy(dst, src, count * sizeof(int));
}

void run_demo(void)
{
    char line[64];
    int source[16];
    int target[6];
    int count;
    int i;

    for (i = 0; i < 16; i++)
    {
        source[i] = i * 3;
    }

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return;
    }

    count = parse_count(line);

    copy_values(target, source, count);

    for (i = 0; i < 6; i++)
    {
        printf("%d\n", target[i]);
    }
}

int main(void)
{
    run_demo();
    return 0;
}