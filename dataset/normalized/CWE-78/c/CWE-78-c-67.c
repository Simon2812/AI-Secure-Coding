#include "std_testcase.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#define OPEN_PIPE _popen
#define CLOSE_PIPE _pclose
#define FILE_PATH "C:\\temp\\file.txt"
#define BASE_CMD "dir "
#else
#include <unistd.h>
#define OPEN_PIPE popen
#define CLOSE_PIPE pclose
#define FILE_PATH "/tmp/file.txt"
#define BASE_CMD "ls "
#endif

void run_file_popen_task(void)
{
    char suffix[80] = {0};
    char cmd[128] = BASE_CMD;
    FILE *f = fopen(FILE_PATH, "r");

    if (f != NULL)
    {
        if (fgets(suffix, sizeof(suffix), f) != NULL)
        {
            size_t i;
            for (i = 0; suffix[i] != '\0'; ++i)
            {
                if (!((suffix[i] >= 'a' && suffix[i] <= 'z') ||
                      (suffix[i] >= 'A' && suffix[i] <= 'Z') ||
                      (suffix[i] >= '0' && suffix[i] <= '9') ||
                      suffix[i] == '.' || suffix[i] == '_' ||
                      suffix[i] == '-' || suffix[i] == '/'))
                {
                    suffix[i] = '\0';
                    break;
                }
            }
        }
        fclose(f);
    }

    strncat(cmd, suffix, sizeof(cmd) - strlen(cmd) - 1);

    FILE *p = OPEN_PIPE(cmd, "r");
    if (p) CLOSE_PIPE(p);
}