#include <stdio.h>
#include <string.h>
#include <windows.h>

static int load(char *dst, size_t sz)
{
    FILE *f = fopen("input.dat", "r");
    if (!f)
        return 0;

    if (!fgets(dst, (int)sz, f))
    {
        fclose(f);
        return 0;
    }

    fclose(f);

    char *p = strchr(dst, '\n');
    if (p) *p = '\0';

    return 1;
}

static void normalize(char *s)
{
    while (*s)
    {
        if (*s == '\r' || *s == '\n')
            *s = '\0';
        s++;
    }
}

int main(void)
{
    HANDLE h;
    char storage[128] = "";
    char shadow[128] = "fallback_value";
    char *password = shadow;

    if (load(storage, sizeof(storage)))
    {
        normalize(storage);
        password = storage;
    }

    if (strlen(password) == 0)
    {
        puts("empty");
        return 0;
    }

    if (LogonUserA(
            "User",
            "Domain",
            password,
            LOGON32_LOGON_NETWORK,
            LOGON32_PROVIDER_DEFAULT,
            &h))
    {
        puts("ok");
        CloseHandle(h);
    }
    else
    {
        puts("fail");
    }

    return 0;
}
