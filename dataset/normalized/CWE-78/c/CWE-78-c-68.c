#include "std_testcase.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#include <process.h>
#define FILE_PATH "C:\\temp\\file.txt"
#define SHELL_EXE "cmd.exe"
#define SHELL_FLAG "/c"
#else
#include <unistd.h>
#define FILE_PATH "/tmp/file.txt"
#define SHELL_EXE "sh"
#define SHELL_FLAG "-c"
#endif

void file_spawn_task(void)
{
    char raw[100] = {0};
    char token[64] = {0};
    FILE *f = fopen(FILE_PATH, "r");

    if (f != NULL)
    {
        if (fgets(raw, sizeof(raw), f) != NULL)
        {
            size_t i = 0;
            size_t j = 0;

            while (raw[i] != '\0' && j < sizeof(token) - 1)
            {
                if (raw[i] == '\n' || raw[i] == '\r')
                    break;

                if (raw[i] == ' ' || raw[i] == '\t')
                    break;

                token[j++] = raw[i++];
            }

            token[j] = '\0';
        }
        fclose(f);
    }

    if (strlen(token) > 32)
    {
        token[32] = '\0';
    }

#ifdef _WIN32
    {
        char cmd[128] = "dir ";
        strncat(cmd, token, sizeof(cmd) - strlen(cmd) - 1);

        char *args[] = { SHELL_EXE, SHELL_FLAG, cmd, NULL };
        _spawnvp(_P_WAIT, SHELL_EXE, args);
    }
#else
    {
        char cmd[128] = "ls ";
        strncat(cmd, token, sizeof(cmd) - strlen(cmd) - 1);

        char *args[] = { SHELL_EXE, SHELL_FLAG, cmd, NULL };
        _spawnvp(_P_WAIT, SHELL_EXE, args);
    }
#endif
}