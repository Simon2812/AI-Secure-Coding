#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <process.h>
#define EXECVP _execvp
#define COMMAND_INT "cmd.exe"
#define COMMAND_INT_PATH "%WINDIR%\\system32\\cmd.exe"
#define COMMAND_ARG1 "/c"
#define COMMAND_ARG2 "tree "
#define COMMAND_ARG3 data
#define GETENV getenv
#else
#include <unistd.h>
#define EXECVP execvp
#define COMMAND_INT "sh"
#define COMMAND_INT_PATH "/bin/sh"
#define COMMAND_ARG1 "-c"
#define COMMAND_ARG2 "find . -maxdepth 1 -name "
#define COMMAND_ARG3 data
#define GETENV getenv
#endif

#define ENV_VARIABLE "ADD"

void run_env_query(void)
{
    char dataBuffer[100] = COMMAND_ARG2;
    char *data = dataBuffer;

    size_t dataLen = strlen(data);
    char *environment = GETENV(ENV_VARIABLE);

    if (environment != NULL)
        strncat(data + dataLen, environment, 100 - dataLen - 1);

    {
        char *args[] = { COMMAND_INT_PATH, COMMAND_ARG1, COMMAND_ARG3, NULL };
        EXECVP(COMMAND_INT, args);
    }
}