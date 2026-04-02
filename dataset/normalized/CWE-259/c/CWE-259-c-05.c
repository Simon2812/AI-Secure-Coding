#include <stdio.h>
#include <wchar.h>
#include <windows.h>

#define PASSWORD L"managerToken88"

void process_login()
{
    wchar_t storage[100] = L"";
    wchar_t *input = storage;

    if (1)
    {
        wcscpy(input, PASSWORD);
    }

    {
        HANDLE session;
        wchar_t *account = L"User";
        wchar_t *domain = L"Domain";

        if (LogonUserW(
                account,
                domain,
                input,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &session) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(session);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    process_login();
    return 0;
}