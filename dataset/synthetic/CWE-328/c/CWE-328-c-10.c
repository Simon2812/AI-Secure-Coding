#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_MAX 128
#define HASH_LEN (160 / 8)

static int read_reference(UCHAR *out, size_t len)
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
        out[i] = (UCHAR)v;
    }

    fclose(f);
    return 1;
}

static void trim(char *buf)
{
    size_t n = strcspn(buf, "\r\n");
    buf[n] = '\0';
}

int main(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH h = 0;
    char input[INPUT_MAX];
    UCHAR expected[HASH_LEN];
    UCHAR actual[HASH_LEN];
    DWORD actualLen = HASH_LEN;

    if (!read_reference(expected, HASH_LEN))
    {
        return 1;
    }

    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        return 1;
    }

    trim(input);

    if (!CryptAcquireContextW(&prov, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(prov, CALG_RIPEMD160, 0, 0, &h))
    {
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptHashData(h, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptGetHashParam(h, HP_HASHVAL, actual, &actualLen, 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (memcmp(expected, actual, HASH_LEN) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    CryptDestroyHash(h);
    CryptReleaseContext(prov, 0);
    return 0;
}