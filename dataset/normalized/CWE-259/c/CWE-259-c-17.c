#include <stdio.h>
#include <wchar.h>
#include <stdlib.h>
#include <windows.h>

#define PASSWORD _wgetenv(L"APP_PASSWORD")

int main(void)
{
    wchar_t buffer[100] = L"";
    wchar_t *password = buffer;
    wchar_t *source = PASSWORD;
    HANDLE handle;
    wchar_t *username = L"User";
    wchar_t *domain = L"Domain";

    if (source != NULL)
    {
        wcscpy(password, source);
    }
    else
    {
        password[0] = L'\0';
    }

    if (LogonUserW(
            username,
            domain,
            password,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &handle) != 0)
    {
        puts("User logged in successfully.");
        CloseHandle(handle);
    }
    else
    {
        puts("Unable to login.");
    }

    return 0;
}