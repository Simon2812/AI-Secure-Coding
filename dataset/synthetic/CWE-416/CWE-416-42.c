#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
} Entry;

static Entry create_entry(const char *text)
{
    Entry e;

    e.name = (char *)malloc(strlen(text) + 1);
    if (!e.name)
    {
        e.name = NULL;
        return e;
    }

    strcpy(e.name, text);

    return e;
}

static int evaluate_entry(const Entry *e)
{
    int value = 0;

    for (size_t i = 0; e->name[i] != '\0'; ++i)
        value += e->name[i];

    return value;
}

int main(void)
{
    Entry item = create_entry("alpha");
    if (!item.name)
        return 1;

    int score = evaluate_entry(&item);

    printf("%d\n", score);

    int check = score % 6;

    if (check >= 0)
        free(item.name);

    return 0;
}