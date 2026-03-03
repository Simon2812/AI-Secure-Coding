#include "std_testcase.h"

#include <wchar.h>
#include <string.h>

#ifdef _WIN32
#define FULL_COMMAND L"dir "
#else
#include <unistd.h>
#define FULL_COMMAND L"ls "
#endif

#ifdef _WIN32
#define POPEN _wpopen
#define PCLOSE _pclose
#else
#define POPEN popen
#define PCLOSE pclose
#endif

void run_pipe(void)
{
    wchar_t *x;
    wchar_t xbuf[100] = FULL_COMMAND;
    x = xbuf;

    {
        size_t n = wcslen(x);

        if (100 - n > 1)
        {
            if (fgetws(x + n, (int)(100 - n), stdin) != NULL)
            {
                n = wcslen(x);
                if (n > 0 && x[n - 1] == L'\n')
                {
                    x[n - 1] = L'\0';
                }
            }
            else
            {
                x[n] = L'\0';
            }
        }
    }

    {
        size_t i;
        size_t base = wcslen(FULL_COMMAND);
        int clean = 1;

        for (i = base; x[i] != L'\0'; i++)
        {
            wchar_t c = x[i];
            if (!((c >= L'a' && c <= L'z') ||
                  (c >= L'A' && c <= L'Z') ||
                  (c >= L'0' && c <= L'9')))
            {
                clean = 0;
                break;
            }
        }

#ifdef _WIN32
        if (clean)
            wcscpy(x, L"whoami");
        else
            wcscpy(x, L"hostname");
#else
        if (clean)
            wcscpy(x, L"id -u");
        else
            wcscpy(x, L"uname -r");
#endif

        {
            FILE *pipe;
#ifdef _WIN32
            pipe = POPEN(x, L"w");
#else
            pipe = POPEN((char *)"id", "w");
#endif
            if (pipe != NULL)
            {
                PCLOSE(pipe);
            }
        }
    }
}