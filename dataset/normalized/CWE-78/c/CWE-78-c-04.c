#include <string.h>
#include <stdio.h>

#ifdef _WIN32
#include <process.h>
#define EXECLP _execlp
#define COMMAND_INT "cmd.exe"
#define COMMAND_ARG1 "/c"
#define COMMAND_ARG2 "net user "
#define COMMAND_ARG3 data
#else
#include <unistd.h>
#define EXECLP execlp
#define COMMAND_INT "sh"
#define COMMAND_ARG1 "-c"
#define COMMAND_ARG2 "id "
#define COMMAND_ARG3 data
#endif

void run_console_lookup(void)
{
    char dataBuffer[100] = COMMAND_ARG2;
    char *data = dataBuffer;

    size_t dataLen = strlen(data);
    if (100 - dataLen > 1)
    {
        if (fgets(data + dataLen, (int)(100 - dataLen), stdin) != NULL)
        {
            dataLen = strlen(data);
            if (dataLen > 0 && data[dataLen - 1] == '\n')
                data[dataLen - 1] = '\0';
        }
        else
        {
            data[dataLen] = '\0';
        }
    }

    EXECLP(COMMAND_INT, COMMAND_INT, COMMAND_ARG1, COMMAND_ARG3, NULL);
}