#include <wchar.h>
#include <stdlib.h>
#include <string.h>

#define FULL_COMMAND L"tasklist "
#define FILENAME "C:\\temp\\file.txt"

#define POPEN _wpopen
#define PCLOSE _pclose

void wide_file_popen(void)
{
    wchar_t data_buf[100] = FULL_COMMAND;
    wchar_t *data = data_buf;

    size_t dataLen = wcslen(data);
    FILE *pFile;

    if (100 - dataLen > 1)
    {
        pFile = fopen(FILENAME, "r");
        if (pFile != NULL)
        {
            if (fgetws(data + dataLen, (int)(100 - dataLen), pFile) == NULL)
            {
                data[dataLen] = L'\0';
            }
            fclose(pFile);
        }
    }

    {
        FILE *pipe;
        pipe = POPEN(data, L"w");
        if (pipe != NULL)
        {
            PCLOSE(pipe);
        }
    }
}