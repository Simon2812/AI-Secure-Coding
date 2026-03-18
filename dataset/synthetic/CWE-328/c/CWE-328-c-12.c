#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define LIMIT 128
#define OUT_SIZE (128 / 8)

static int read_file(UCHAR *buf, size_t len)
{
    FILE *f = fopen("password.txt", "r");
    size_t i;

    if (!f)
    {
        return 0;
    }

    for (i = 0; i < len; i++)
    {
        ULONG v;
        if (fscanf(f, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(f);
            return 0;
        }
        buf[i] = (UCHAR)v;
    }

    fclose(f);
    return 1;
}

static int compute_twice(const char *text, UCHAR *out)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH h1 = 0;
    HCRYPTHASH h2 = 0;
    UCHAR temp[OUT_SIZE];
    DWORD len = OUT_SIZE;

    if (!CryptAcquireContextW(&prov, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 0;
    }

    if (!CryptCreateHash(prov, CALG_MD5, 0, 0, &h1))
    {
        CryptReleaseContext(prov, 0);
        return 0;
    }

    if (!CryptHashData(h1, (BYTE *)text, (DWORD)strlen(text), 0))
    {
        CryptDestroyHash(h1);
        CryptReleaseContext(prov, 0);
        return 0;
    }

    if (!CryptGetHashParam(h1, HP_HASHVAL, temp, &len, 0))
    {
        CryptDestroyHash(h1);
        CryptReleaseContext(prov, 0);
        return 0;
    }

    CryptDestroyHash(h1);

    if (!CryptCreateHash(prov, CALG_MD5, 0, 0, &h2))
    {
        CryptReleaseContext(prov, 0);
        return 0;
    }

    len = OUT_SIZE;

    if (!CryptHashData(h2, temp, len, 0))
    {
        CryptDestroyHash(h2);
        CryptReleaseContext(prov, 0);
        return 0;
    }

    if (!CryptGetHashParam(h2, HP_HASHVAL, out, &len, 0))
    {
        CryptDestroyHash(h2);
        CryptReleaseContext(prov, 0);
        return 0;
    }

    CryptDestroyHash(h2);
    CryptReleaseContext(prov, 0);
    return 1;
}

int main(void)
{
    char input[LIMIT];
    UCHAR stored[OUT_SIZE];
    UCHAR produced[OUT_SIZE];

    if (!read_file(stored, OUT_SIZE))
    {
        return 1;
    }

    if (!fgets(input, sizeof(input), stdin))
    {
        return 1;
    }

    input[strcspn(input, "\r\n")] = '\0';

    if (!compute_twice(input, produced))
    {
        return 1;
    }

    if (memcmp(stored, produced, OUT_SIZE) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    return 0;
}