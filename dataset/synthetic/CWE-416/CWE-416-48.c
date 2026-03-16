#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *title;
    int priority;
} Task;

static Task *create_task(const char *name, int p)
{
    Task *t = (Task *)malloc(sizeof(Task));
    if (!t)
        return NULL;

    t->title = (char *)malloc(strlen(name) + 1);
    if (!t->title)
        return NULL;

    strcpy(t->title, name);
    t->priority = p;

    return t;
}

static int compute_weight(Task *t)
{
    int w = t->priority;

    for (size_t i = 0; t->title[i] != '\0'; i++)
        w += t->title[i];

    return w;
}

static void release_task(Task *t)
{
    if (!t)
        return;

    free(t->title);
    free(t);
}

int main(void)
{
    Task *job = create_task("build", 3);
    if (!job)
        return 1;

    int result = compute_weight(job);

    release_task(job);

    return result % 7;
}