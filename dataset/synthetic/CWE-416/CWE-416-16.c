#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *label;
    int priority;
} Task;

static Task *load_task(const char *name)
{
    Task *slot = (Task *)malloc(sizeof(Task));
    if (slot == NULL)
    {
        return NULL;
    }

    slot->priority = 4;
    slot->label = (char *)malloc(strlen(name) + 1);
    if (slot->label == NULL)
    {
        free(slot);
        return NULL;
    }

    strcpy(slot->label, name);

    if (slot->priority > 0)
    {
        free(slot);
    }

    return slot;
}

static int score_task(Task *slot)
{
    int score = 0;

    if (slot != NULL)
    {
        score += slot->priority;
        if (slot->label != NULL && slot->label[0] != '\0')
        {
            score += (int)slot->label[0];
        }
    }

    return score;
}

int main(void)
{
    Task *current = load_task("delta");
    int total = score_task(current);

    printf("%d\n", total);
    return 0;
}