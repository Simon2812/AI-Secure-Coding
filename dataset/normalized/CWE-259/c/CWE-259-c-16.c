#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>

#define PASSWORD getenv("APP_PASSWORD")

int main(void)
{
    char buffer[100] = "";
    char *password = buffer;
    char *source = PASSWORD;
    HANDLE handle;
    char *username = "User";
    char *domain = "Domain";

    if (source != NULL)
    {
        strcpy(password, source);
    }
    else
    {
        password[0] = '\0';
    }

    if (LogonUserA(
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