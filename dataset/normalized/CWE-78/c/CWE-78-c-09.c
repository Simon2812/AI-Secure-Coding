#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <process.h>
#define COMMAND_INT_PATH "%WINDIR%\\system32\\cmd.exe"
#define COMMAND_INT "cmd.exe"
#define COMMAND_ARG1 "/c"
#define COMMAND_ARG2 "wevtutil qe System /c:1 /rd:true /f:text /q:"
#define COMMAND_ARG3 data
#define GETENV getenv
#else
#include <unistd.h>
#define COMMAND_INT_PATH "/bin/sh"
#define COMMAND_INT "sh"
#define COMMAND_ARG1 "-c"
#define COMMAND_ARG2 "grep -n "
#define COMMAND_ARG3 data
#define GETENV getenv
#endif

#define ENV_VARIABLE "ADD"

void env_action(void)
{
    char dataBuffer[100] = COMMAND_ARG2;
    char *data = dataBuffer;

    size_t dataLen = strlen(data);
    char *environment = GETENV(ENV_VARIABLE);

    if (environment != NULL)
        strncat(data + dataLen, environment, 100 - dataLen - 1);

    {
        char *args[] = { COMMAND_INT_PATH, COMMAND_ARG1, COMMAND_ARG3, NULL };
        _spawnvp(_P_WAIT, COMMAND_INT, args);
    }
}