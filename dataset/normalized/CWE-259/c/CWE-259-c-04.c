#include <stdio.h>
#include <wchar.h>
#include <windows.h>

#define PASSWORD L"prodDbSecret"

void initialize_client()
{
    wchar_t buffer[100] = L"";
    wchar_t *secret = buffer;

    wcscpy(secret, PASSWORD);

    {
        HANDLE handle;
        wchar_t *user = L"User";
        wchar_t *domain = L"Domain";

        if (LogonUserW(
                user,
                domain,
                secret,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT,
                &handle) != 0)
        {
            printf("User logged in successfully.\n");
            CloseHandle(handle);
        }
        else
        {
            printf("Unable to login.\n");
        }
    }
}

int main(void)
{
    initialize_client();
    return 0;
}