#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <process.h>
#define EXECLP _wexeclp
#define COMMAND_INT L"cmd.exe"
#define COMMAND_ARG1 L"/c"
#define COMMAND_ARG2 L"where "
#define COMMAND_ARG3 data
#else
#include <unistd.h>
#define EXECLP execlp
#define COMMAND_INT L"sh"
#define COMMAND_ARG1 L"-c"
#define COMMAND_ARG2 L"uname "
#define COMMAND_ARG3 data
#endif

void run_wide_console_exec(void)
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

    EXECLP(COMMAND_INT, COMMAND_INT, COMMAND_ARG1, COMMAND_ARG3, NULL);
}