#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define MAX_LEN 128
#define HASH_SZ 32

static int read_bytes(UCHAR *dst, size_t n)
{
    FILE *f = fopen("password.txt", "r");
    size_t i;

    if (!f)
        return 0;

    for (i = 0; i < n; i++)
    {
        ULONG v;
        if (fscanf(f, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(f);
            return 0;
        }
        dst[i] = (UCHAR)v;
    }

    fclose(f);
    return 1;
}

static int make_digest(const char *input, UCHAR *out)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    DWORD len = HASH_SZ;
    int ok = 0;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 0;

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &h))
    {
        if (!CryptCreateHash(ctx, CALG_MD5, 0, 0, &h))
        {
            CryptReleaseContext(ctx, 0);
            return 0;
        }
    }

    if (!CryptHashData(h, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (CryptGetHashParam(h, HP_HASHVAL, out, &len, 0))
        ok = 1;

    CryptDestroyHash(h);
    CryptReleaseContext(ctx, 0);
    return ok;
}

int main(void)
{
    char buf[MAX_LEN];
    UCHAR expected[HASH_SZ];
    UCHAR result[HASH_SZ];

    if (!read_bytes(expected, HASH_SZ))
        return 1;

    if (!fgets(buf, sizeof(buf), stdin))
        return 1;

    buf[strcspn(buf, "\r\n")] = '\0';

    if (!make_digest(buf, result))
        return 1;

    if (memcmp(expected, result, HASH_SZ) == 0)
        puts("Access granted");
    else
        puts("Access denied");

    return 0;
}