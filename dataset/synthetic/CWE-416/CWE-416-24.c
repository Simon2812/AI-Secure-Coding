#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
} User;

static User *create_user(const char *n)
{
    User *u = (User *)malloc(sizeof(User));
    if (!u)
        return NULL;

    u->name = (char *)malloc(strlen(n) + 1);
    if (!u->name)
    {
        free(u);
        return NULL;
    }

    strcpy(u->name, n);
    return u;
}

static void destroy_user(User *u)
{
    if (!u)
        return;

    if (u->name)
        free(u->name);

    free(u);
}

static int user_score(User *u)
{
    int s = 0;

    for (size_t i = 0; u->name[i] != '\0'; i++)
        s += u->name[i];

    return s;
}

int main(void)
{
    User *a = create_user("guest");
    if (!a)
        return 1;

    User *b = a;

    destroy_user(a);

    int result = user_score(b);

    printf("%d\n", result);

    return 0;
}