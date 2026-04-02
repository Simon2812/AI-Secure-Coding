#include "std_testcase.h"

#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define FULL_COMMAND "whoami"
#else
#include <unistd.h>
#define FULL_COMMAND "id"
#endif

#define SYSTEM system

void run_console_task(void)
{
    char input_buf[100] = {0};
    char *input = input_buf;

    size_t dataLen = 0;
    if (100 - dataLen > 1)
    {
        if (fgets(input + dataLen, (int)(100 - dataLen), stdin) != NULL)
        {
            dataLen = strlen(input);
            if (dataLen > 0 && input[dataLen - 1] == '\n')
            {
                input[dataLen - 1] = '\0';
            }
        }
        else
        {
            input[dataLen] = '\0';
        }
    }

    if (SYSTEM(FULL_COMMAND) != 0)
    {
        printLine("command execution failed!");
        exit(1);
    }
}