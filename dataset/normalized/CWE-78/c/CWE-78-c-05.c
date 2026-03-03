#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#define FULL_COMMAND "tasklist "
#define POPEN _popen
#define PCLOSE _pclose
#else
#include <unistd.h>
#define FULL_COMMAND "ps "
#define POPEN popen
#define PCLOSE pclose
#endif

void run_process_query(void)
{
    char buffer[100] = FULL_COMMAND;
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

    FILE *pipe = POPEN(data, "r");
    if (pipe != NULL)
        PCLOSE(pipe);
}