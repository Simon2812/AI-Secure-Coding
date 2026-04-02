#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define FULL_COMMAND L"whoami "
#define SYSTEM _wsystem
#else
#include <unistd.h>
#define FULL_COMMAND L"id "
#define SYSTEM system
#endif

void run_wide_console_system(void)
{
    wchar_t data_buf[100] = FULL_COMMAND;
    wchar_t *data = data_buf;

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

    if (SYSTEM(data) != 0)
        exit(1);
}