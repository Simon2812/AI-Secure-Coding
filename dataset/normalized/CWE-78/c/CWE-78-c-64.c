#include "std_testcase.h"

#include <wchar.h>
#include <string.h>
#include <stdlib.h>
#include <process.h>

#ifdef _WIN32
#define COMMAND_INT "cmd.exe"
#define COMMAND_ARG1 "/c"
#define FIXED_CMD "whoami"
#else
#include <unistd.h>
#define COMMAND_INT "sh"
#define COMMAND_ARG1 "-c"
#define FIXED_CMD "id"
#endif

void console_spawn_task(void)
{
    char inputBuffer[100] = {0};
    char *input = inputBuffer;

    size_t len = 0;
    if (100 - len > 1)
    {
        if (fgets(input + len, (int)(100 - len), stdin) != NULL)
        {
            len = strlen(input);
            if (len > 0 && input[len - 1] == '\n')
            {
                input[len - 1] = '\0';
            }
        }
        else
        {
            input[len] = '\0';
        }
    }

#ifdef _WIN32
    _spawnlp(_P_WAIT, COMMAND_INT, COMMAND_INT, COMMAND_ARG1, FIXED_CMD, NULL);
#else
    _spawnlp(_P_WAIT, COMMAND_INT, COMMAND_INT, COMMAND_ARG1, FIXED_CMD, NULL);
#endif
}