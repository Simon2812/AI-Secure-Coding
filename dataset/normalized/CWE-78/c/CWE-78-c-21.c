#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define COMMAND_INT_PATH L"%WINDIR%\\system32\\cmd.exe"
#define COMMAND_INT L"cmd.exe"
#define COMMAND_ARG1 L"/c"
#define COMMAND_ARG2 L"echo "
#else
#include <unistd.h>
#define COMMAND_INT_PATH L"/bin/sh"
#define COMMAND_INT L"sh"
#define COMMAND_ARG1 L"-c"
#define COMMAND_ARG2 L"printf "
#endif

#include <process.h>

void wide_console_spawnv(void)
{
    wchar_t dataBuffer[100] = COMMAND_ARG2;
    wchar_t *data = dataBuffer;

    size_t dataLen = wcslen(data);

    if (100 - dataLen > 1)
    {
        if (fgetws(data + dataLen, (int)(100 - dataLen), stdin) != NULL)
        {
            dataLen = wcslen(data);
            if (dataLen > 0 && data[dataLen - 1] == L'\n')
                data[dataLen - 1] = L'\0';
        }
        else
        {
            data[dataLen] = L'\0';
        }
    }

    wchar_t *args[] = {
        COMMAND_INT_PATH,
        COMMAND_ARG1,
        data,
        NULL
    };

    _wspawnv(_P_WAIT, COMMAND_INT_PATH, args);
}