#include <stdio.h>
#include <wchar.h>
#include <windows.h>

int main(void)
{
    wchar_t buffer[100] = L"";
    wchar_t *password = buffer;
    HANDLE handle;
    FILE *f = _wfopen(L"password.txt", L"r");

    if (f != NULL)
    {
        if (fgetws(password, 100, f) != NULL)
        {
            size_t len = wcslen(password);
            if (len > 0 && password[len - 1] == L'\n')
            {
                password[len - 1] = L'\0';
            }
        }
        fclose(f);
    }
    else
    {
        password[0] = L'\0';
    }

    if (LogonUserW(
            L"User",
            L"Domain",
            password,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &handle))
    {
        puts("ok");
        CloseHandle(handle);
    }
    else
    {
        puts("fail");
    }

    return 0;
}
