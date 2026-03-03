#include "std_testcase.h"

#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define PREFIX L"cmd /c "
#define GETENV _wgetenv
#define CALL _wsystem
#else
#include <unistd.h>
#define PREFIX L"sh -c "
#define GETENV getenv
#define CALL system
#endif

#define VAR_NAME L"ADD"

void system_query(void)
{
    wchar_t *q;
    wchar_t qbuf[100] = PREFIX;
    q = qbuf;

    {
        size_t n = wcslen(q);
        wchar_t *env = GETENV(VAR_NAME);

        if (env != NULL)
        {
            wcsncat(q + n, env, 100 - n - 1);
        }
    }

    {
        size_t i;
        size_t start = wcslen(PREFIX);
        int ok = 1;

        for (i = start; q[i] != L'\0'; i++)
        {
            wchar_t c = q[i];
            if (!((c >= L'a' && c <= L'z') ||
                  (c >= L'A' && c <= L'Z') ||
                  (c >= L'0' && c <= L'9')))
            {
                ok = 0;
                break;
            }
        }

#ifdef _WIN32
        if (ok)
            wcscpy(q, L"cmd /c echo ready");
        else
            wcscpy(q, L"cmd /c ver");
#else
        if (ok)
            wcscpy(q, L"sh -c printf_ok");
        else
            wcscpy(q, L"sh -c uname");
#endif

        if (CALL(q) != 0)
        {
            printLine("execution failed");
            exit(1);
        }
    }
}