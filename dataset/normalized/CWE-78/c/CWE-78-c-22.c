#include <wchar.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>

#define ENV_VARIABLE L"ADD"
#define GETENV _wgetenv
#define EXECL _wexecl

#define COMMAND_ARG2 L"where "

void wide_env_execl(void)
{
    wchar_t dataBuffer[100] = COMMAND_ARG2;
    wchar_t *data = dataBuffer;

    size_t dataLen = wcslen(data);
    wchar_t *environment = GETENV(ENV_VARIABLE);

    if (environment != NULL)
    {
        wcsncat(data + dataLen, environment, 100 - dataLen - 1);
    }

    EXECL(L"%WINDIR%\\system32\\cmd.exe", L"%WINDIR%\\system32\\cmd.exe", L"/c", data, NULL);
}