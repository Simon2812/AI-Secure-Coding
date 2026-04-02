#include <stdio.h>
#include <string.h>
#include <windows.h>

void start_connection()
{
    char buffer[128] = "";
    char *credential = buffer;

    char *rawValue = "admin123!";
    char *copySource = rawValue;

    strcpy(credential, copySource);

    {
        HANDLE handle;
        char *account = "User";
        char *realm = "Domain";

        if (LogonUserA(
                account,
                realm,
                credential,
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
    start_connection();
    return 0;
}