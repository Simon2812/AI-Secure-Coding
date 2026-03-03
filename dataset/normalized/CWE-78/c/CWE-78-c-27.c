#include <wchar.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#define COMMAND_INT_PATH L"%WINDIR%\\system32\\cmd.exe"
#define COMMAND_INT L"cmd.exe"
#define COMMAND_ARG1 L"/c"
#define COMMAND_ARG2 L"whoami "
#define FILENAME "C:\\temp\\file.txt"

void wide_file_spawnvp(void)
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

    {
        wchar_t *args[] = { COMMAND_INT_PATH, COMMAND_ARG1, data, NULL };
        _wspawnvp(_P_WAIT, COMMAND_INT, args);
    }
}