#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#define FULL_COMMAND "dir "
#define FILENAME "C:\\temp\\file.txt"
#define SYSTEM system
#else
#include <unistd.h>
#define FULL_COMMAND "ls "
#define FILENAME "/tmp/file.txt"
#define SYSTEM system
#endif

void file_scan(void)
{
    char data_buf[100] = FULL_COMMAND;
    char *data = data_buf;

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

    if (SYSTEM(data) != 0)
        exit(1);
}