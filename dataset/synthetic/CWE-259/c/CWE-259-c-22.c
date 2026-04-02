#include <stdio.h>
#include <string.h>
#include <windows.h>

int main(void)
{
    HANDLE h;
    char input[128];
    char *u = "User";
    char *d = "Domain";

    FILE *fp = fopen("cred.txt", "r");
    if (!fp)
    {
        puts("no file");
        return 0;
    }

    if (!fgets(input, sizeof(input), fp))
    {
        fclose(fp);
        return 0;
    }
    fclose(fp);

    char *nl = strchr(input, '\n');
    if (nl) *nl = '\0';

    if (LogonUserA(
            u,
            d,
            input,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &h))
    {
        puts("ok");
        CloseHandle(h);
    }
    else
    {
        puts("Failed...");
    }

    return 0;
}