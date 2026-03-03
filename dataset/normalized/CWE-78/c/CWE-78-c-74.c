#include "std_testcase.h"
#include <wchar.h>

#ifdef _WIN32
#include <process.h>
#endif

void execute_task(void)
{
#ifdef _WIN32
    wchar_t buf[100] = L"";
    size_t n = 0;

    if (100 - n > 1)
    {
        if (fgetws(buf + n, (int)(100 - n), stdin) != NULL)
        {
            n = wcslen(buf);
            if (n > 0 && buf[n - 1] == L'\n')
            {
                buf[n - 1] = L'\0';
            }
        }
        else
        {
            buf[n] = L'\0';
        }
    }

    {
        const wchar_t *cmd = L"whoami";
        wchar_t *args_who[] = {L"whoami", NULL};
        wchar_t *args_tasks[] = {L"tasklist", L"/fo", L"csv", NULL};

        if (wcscmp(buf, L"tasks") == 0 || wcscmp(buf, L"2") == 0)
        {
            cmd = L"tasklist";
            _wexecvp(cmd, args_tasks);
        }
        else
        {
            _wexecvp(cmd, args_who);
        }
    }
#else
    (void)0;
#endif
}