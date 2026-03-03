#include <string.h>
#include <stdio.h>

#ifdef _WIN32
#include <process.h>
#define EXECLP _execlp
#define COMMAND_INT "cmd.exe"
#define COMMAND_ARG1 "/c"
#define COMMAND_ARG2 "dir "
#define COMMAND_ARG3 data
#define FILENAME "C:\\temp\\file.txt"
#else
#include <unistd.h>
#define EXECLP execlp
#define COMMAND_INT "sh"
#define COMMAND_ARG1 "-c"
#define COMMAND_ARG2 "ls "
#define COMMAND_ARG3 data
#define FILENAME "/tmp/file.txt"
#endif

void run_file_listing(void)
{
    char dataBuffer[100] = COMMAND_ARG2;
    char *data = dataBuffer;

    size_t dataLen = strlen(data);
    FILE *pFile;

    if (100 - dataLen > 1)
    {
        pFile = fopen(FILENAME, "r");
        if (pFile != NULL)
        {
            if (fgets(data + dataLen, (int)(100 - dataLen), pFile) == NULL)
                data[dataLen] = '\0';
            fclose(pFile);
        }
    }

    EXECLP(COMMAND_INT, COMMAND_INT, COMMAND_ARG1, COMMAND_ARG3, NULL);
}