#include <stdio.h>
#include <string.h>
#include <windows.h>

int main(void)
{
    char buffer[100] = "";
    char *password = buffer;
    HANDLE handle;
    FILE *f = fopen("passwd.txt", "r");

    if (f != NULL)
    {
        if (fgets(password, sizeof(buffer), f) != NULL)
        {
            size_t len = strlen(password);
            if (len > 0 && password[len - 1] == '\n')
            {
                password[len - 1] = '\0';
            }
        }
        fclose(f);
    }
    else
    {
        password[0] = '\0';
    }

    if (LogonUserA(
            "User",
            "Domain",
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