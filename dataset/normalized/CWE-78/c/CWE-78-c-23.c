#include "std_testcase.h"
#include <wchar.h>
#include <stdlib.h>
#include <process.h>

#define ENV_KEY L"ADD"

static void run_case(void)
{
    wchar_t prefix[32] = L"whoami ";
    wchar_t buf[128];
    wchar_t *p;
    size_t n;

    buf[0] = L'\0';
    wcscat(buf, prefix);

    p = _wgetenv(ENV_KEY);
    if (p != NULL)
    {
        n = wcslen(buf);
        wcsncat(buf + n, p, (sizeof(buf) / sizeof(buf[0])) - n - 1);
    }

    _wpopen(buf, L"w");
}