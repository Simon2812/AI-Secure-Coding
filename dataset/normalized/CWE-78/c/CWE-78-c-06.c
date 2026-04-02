#include <string.h>
#include <stdio.h>

#ifdef _WIN32
#include <process.h>
#define EXECV _execv
#define CMD_PATH "%WINDIR%\\system32\\cmd.exe"
#define CMD_FLAG "/c"
#define PREFIX "dir "
#else
#include <unistd.h>
#define EXECV execv
#define CMD_PATH "/bin/sh"
#define CMD_FLAG "-c"
#define PREFIX "ls "
#endif

void run_console_listing(void)
{
    char buffer[100] = PREFIX;
    char *data = buffer;

    size_t len = strlen(data);
    if (100 - len > 1)
    {
        if (fgets(data + len, (int)(100 - len), stdin) != NULL)
        {
            len = strlen(data);
            if (len > 0 && data[len - 1] == '\n')
                data[len - 1] = '\0';
        }
        else
        {
            data[len] = '\0';
        }
    }

    char *args[] = { CMD_PATH, CMD_FLAG, data, NULL };
    EXECV(CMD_PATH, args);
}