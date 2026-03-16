#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
} Message;

static void destroy(Message *m)
{
    if (m->text)
        free(m->text);
}

static int decide(Message *m)
{
    if (m->text[0] == 'X')
        return 1;
    return 0;
}

int main(void)
{
    Message msg;
    msg.text = malloc(16);

    if (!msg.text)
        return 1;

    strcpy(msg.text, "XYZ");

    int flag = rand() % 2;

    if (flag)
        destroy(&msg);

    int outcome = decide(&msg);

    printf("%d\n", outcome);

    return 0;
}