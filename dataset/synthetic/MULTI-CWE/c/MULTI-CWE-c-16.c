#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char username[32];
    char password[32];
    char target[128];
} Session;

static void init_session(Session *s)
{
    strncpy(s->username, "user", sizeof(s->username) - 1);
    s->username[sizeof(s->username) - 1] = '\0';

    strncpy(s->password, "pass123", sizeof(s->password) - 1);
    s->password[sizeof(s->password) - 1] = '\0';

    strncpy(s->target, ".", sizeof(s->target) - 1);
    s->target[sizeof(s->target) - 1] = '\0';
}

static void load_session(Session *s, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(s->password, argv[1], sizeof(s->password) - 1);
        s->password[sizeof(s->password) - 1] = '\0';
    }

    if (argc > 2)
    {
        strncpy(s->target, argv[2], sizeof(s->target) - 1);
        s->target[sizeof(s->target) - 1] = '\0';
    }
}

static int authenticate(const Session *s)
{
    const char *stored = "admin123";

    if (strcmp(s->password, stored) == 0)
    {
        return 1;
    }

    return 0;
}

static void run_task(const char *target)
{
    char command[256];

    snprintf(command, sizeof(command), "ls %s", target);
    system(command);
}

int main(int argc, char *argv[])
{
    Session session;

    init_session(&session);
    load_session(&session, argc, argv);

    if (authenticate(&session))
    {
        printf("Authorized\n");
        run_task(session.target);
    }
    else
    {
        printf("Denied\n");
    }

    return 0;
}