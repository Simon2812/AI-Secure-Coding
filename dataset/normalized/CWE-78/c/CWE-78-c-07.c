#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define FULL_COMMAND "dir "
#define GETENV getenv
#define SYSTEM system
#else
#include <unistd.h>
#define FULL_COMMAND "ls "
#define GETENV getenv
#define SYSTEM system
#endif

#define ENV_VARIABLE "ADD"

void run_env_listing(void)
{
    char data_buf[100] = FULL_COMMAND;
    char *data = data_buf;

    size_t dataLen = strlen(data);
    char *environment = GETENV(ENV_VARIABLE);

    if (environment != NULL)
        strncat(data + dataLen, environment, 100 - dataLen - 1);

    if (SYSTEM(data) != 0)
        exit(1);
}