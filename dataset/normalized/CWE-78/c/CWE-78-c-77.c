#include "std_testcase.h"

#include <wchar.h>

#ifdef _WIN32
#define COMMAND_INT_PATH L"%WINDIR%\\system32\\cmd.exe"
#define COMMAND_INT L"cmd.exe"
#define COMMAND_ARG1 L"/c"
#define COMMAND_ARG2 L"dir "
#define COMMAND_ARG3 data
#else
#include <unistd.h>
#define COMMAND_INT_PATH L"/bin/sh"
#define COMMAND_INT L"sh"
#define COMMAND_ARG1 L"-c"
#define COMMAND_ARG2 L"ls "
#define COMMAND_ARG3 data
#endif

#ifdef _WIN32
#define FILENAME "C:\\temp\\file.txt"
#else
#define FILENAME "/tmp/file.txt"
#endif

#ifdef _WIN32
#include <process.h>
#define EXECLP _wexeclp
#else
#define EXECLP execlp
#endif

void echo_orbit_launcher(void)
{
    wchar_t * data;
    wchar_t dataBuffer[100] = COMMAND_ARG2;
    data = dataBuffer;

    {
        size_t dataLen = wcslen(data);
        FILE * pFile;

        if (100-dataLen > 1)
        {
            pFile = fopen(FILENAME, "r");
            if (pFile != NULL)
            {
                if (fgetws(data+dataLen, (int)(100-dataLen), pFile) == NULL)
                {
                    data[dataLen] = L'\0';
                }
                fclose(pFile);
            }
        }
    }

    {
        EXECLP(
            COMMAND_INT,
            COMMAND_INT,
            COMMAND_ARG1,
#ifdef _WIN32
            L"whoami",
#else
            L"id",
#endif
            NULL
        );
    }
}