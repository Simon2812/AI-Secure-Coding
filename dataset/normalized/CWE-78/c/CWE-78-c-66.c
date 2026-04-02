#include "std_testcase.h"
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <process.h>
#define DO_SPAWN _spawnlp
#define WAIT_FLAG _P_WAIT
#else
#include <unistd.h>
#define DO_SPAWN spawnlp
#define WAIT_FLAG P_WAIT
#endif

#define ENV_KEY "ADD"

void run_env_spawnlp_task(void)
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
        DO_SPAWN(WAIT_FLAG, "ipconfig", "ipconfig", NULL);
    }
    else if (strcmp(buf, "proc") == 0)
    {
        DO_SPAWN(WAIT_FLAG, "tasklist", "tasklist", NULL);
    }
    else
    {
        DO_SPAWN(WAIT_FLAG, "whoami", "whoami", NULL);
    }
#else
    if (strcmp(buf, "sys") == 0)
    {
        DO_SPAWN(WAIT_FLAG, "uname", "uname", "-a", NULL);
    }
    else if (strcmp(buf, "ls") == 0)
    {
        DO_SPAWN(WAIT_FLAG, "ls", "ls", "-la", NULL);
    }
    else
    {
        DO_SPAWN(WAIT_FLAG, "id", "id", NULL);
    }
#endif
}