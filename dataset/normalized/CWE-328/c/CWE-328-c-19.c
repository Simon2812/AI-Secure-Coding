#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_SIZE 128
#define HASH_SIZE (256 / 8)

static int read_data(UCHAR *buf, size_t len)
{
    FILE *f = fopen("password.txt", "r");
    size_t i;

    if (!f)
        return 0;

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

static void strip(char *s)
{
    char *p = strchr(s, '\n');
    if (p) *p = '\0';
    p = strchr(s, '\r');
    if (p) *p = '\0';
}

int main(void)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    char input[INPUT_SIZE];
    UCHAR expected[HASH_SIZE];
    UCHAR result[HASH_SIZE];
    DWORD size = HASH_SIZE;

    if (!read_data(expected, HASH_SIZE))
        return 1;

    if (!fgets(input, sizeof(input), stdin))
        return 1;

    strip(input);

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &h))
    {
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (!CryptHashData(h, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (!CryptGetHashParam(h, HP_HASHVAL, result, &size, 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (memcmp(expected, result, HASH_SIZE) == 0)
        puts("Access granted");
    else
        puts("Access denied");

    CryptDestroyHash(h);
    CryptReleaseContext(ctx, 0);
    return 0;
}