#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct
{
    int count;
    char label[64];
} Task;

static void init_task(Task *task)
{
    task->count = 8;

    strncpy(task->label, "batch", sizeof(task->label) - 1);
    task->label[sizeof(task->label) - 1] = '\0';
}

static void load_task(Task *task, int argc, char *argv[])
{
    if (argc > 1)
    {
        task->count = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(task->label, argv[2], sizeof(task->label) - 1);
        task->label[sizeof(task->label) - 1] = '\0';
    }
}

static int compute_size(int count)
{
    return count * (int)sizeof(int);
}

static int *allocate_items(int size)
{
    if (size <= 0)
    {
        return NULL;
    }

    return (int *)malloc((size_t)size);
}

static void fill_items(int *items, int count)
{
    int i;

    if (items == NULL)
    {
        return;
    }

    for (i = 0; i < count; i++)
    {
        items[i] = i;
    }
}

static void release_items(int *items)
{
    if (items != NULL)
    {
        free(items);
    }
}

static void print_items(int *items, int count)
{
    if (items == NULL || count <= 0)
    {
        return;
    }

    printf("First: %d\n", items[0]);
}

int main(int argc, char *argv[])
{
    Task task;
    int size;
    int *items;

    init_task(&task);
    load_task(&task, argc, argv);

    size = compute_size(task.count);
    items = allocate_items(size);

    fill_items(items, task.count);

    release_items(items);

    print_items(items, task.count);

    return 0;
}