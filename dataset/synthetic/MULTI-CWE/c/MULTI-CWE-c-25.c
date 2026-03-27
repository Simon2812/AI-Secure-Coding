#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char username[32];
    char password[32];
    char file[128];
    char buffer[64];
} Session;

static void init_session(Session *s)
{
    strncpy(s->username, "guest", sizeof(s->username) - 1);
    s->username[sizeof(s->username) - 1] = '\0';

    strncpy(s->password, "g7H2k9Lp", sizeof(s->password) - 1);
    s->password[sizeof(s->password) - 1] = '\0';

    strncpy(s->file, "/tmp", sizeof(s->file) - 1);
    s->file[sizeof(s->file) - 1] = '\0';

    strncpy(s->buffer, "log:", sizeof(s->buffer) - 1);
    s->buffer[sizeof(s->buffer) - 1] = '\0';
}

static void load_session(Session *s, int argc, char *argv[])
{
    if (argc > 1)
    {
        strncpy(s->file, argv[1], sizeof(s->file) - 1);
        s->file[sizeof(s->file) - 1] = '\0';
    }

    if (argc > 2)
    {
        int offset = strlen(s->buffer);
        int i = 0;

        while (argv[2][i] != '\0')
        {
            s->buffer[offset + i] = argv[2][i];
            i++;
        }

        s->buffer[offset + i] = '\0';
    }

    if (argc > 3)
    {
        strncpy(s->password, argv[3], sizeof(s->password) - 1);
        s->password[sizeof(s->password) - 1] = '\0';
    }
}

static int authenticate(const Session *s)
{
    const char *stored = "A9xT7v2Q";

    if (strcmp(s->password, stored) == 0)
    {
        return 1;
    }

    return 0;
}

static void run_task(const char *file)
{
    char cmd[256] = "cat ";
    strcat(cmd, file);
    system(cmd);
}

static void print_info(const Session *s)
{
    printf("User: %s\n", s->username);
    printf("Buffer: %s\n", s->buffer);
    printf("File: %s\n", s->file);
}

int main(int argc, char *argv[])
{
    Session s;

    init_session(&s);
    load_session(&s, argc, argv);

    print_info(&s);

    if (authenticate(&s))
    {
        run_task(s.file);
    }

    return 0;
}