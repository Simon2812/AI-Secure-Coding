#include "std_testcase.h"
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <process.h>
#define DO_EXECLP _execlp
#define ENV_KEY "ADD"
#else
#include <unistd.h>
#define DO_EXECLP execlp
#define ENV_KEY "ADD"
#endif

void run_env_execlp_task(void)
{
    char buf[100] = {0};
    char *e = getenv(ENV_KEY);

    if (e != NULL)
    {
        strncpy(buf, e, sizeof(buf) - 1);
        buf[sizeof(buf) - 1] = '\0';
    }

#ifdef _WIN32
    if (strcmp(buf, "net") == 0)
    {
        DO_EXECLP("ipconfig", "ipconfig", NULL);
    }
    else if (strcmp(buf, "proc") == 0)
    {
        DO_EXECLP("tasklist", "tasklist", NULL);
    }
    else
    {
        DO_EXECLP("whoami", "whoami", NULL);
    }
#else
    if (strcmp(buf, "sys") == 0)
    {
        DO_EXECLP("uname", "uname", "-a", NULL);
    }
    else if (strcmp(buf, "ls") == 0)
    {
        DO_EXECLP("ls", "ls", "-la", NULL);
    }
    else
    {
        DO_EXECLP("id", "id", NULL);
    }
#endif
}