#include <wchar.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#define COMMAND_ARG2 L"where "
#define FILENAME "C:\\temp\\file.txt"
#define EXECVP _wexecvp

void run_wide_file_execvp(void)
{
    wchar_t dataBuffer[100] = COMMAND_ARG2;
    wchar_t *data = dataBuffer;

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

    wchar_t *args[] = { L"%WINDIR%\\system32\\cmd.exe", L"/c", data, NULL };
    EXECVP(L"cmd.exe", args);
}