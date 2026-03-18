#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define SIZE 128
#define HASH_LEN (256 / 8)

static int load(UCHAR *buf, size_t n)
{
    FILE *f = fopen("password.txt", "r");
    size_t i;

    if (!f) return 0;

    for (i = 0; i < n; i++)
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

static int compute(const char *input, UCHAR *out)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    DWORD len = HASH_LEN;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 0;

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &h))
    {
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (!CryptHashData(h, (BYTE*)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (!CryptGetHashParam(h, HP_HASHVAL, out, &len, 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    CryptDestroyHash(h);
    CryptReleaseContext(ctx, 0);
    return 1;
}

int main(void)
{
    char buf[SIZE];
    UCHAR a[HASH_LEN], b[HASH_LEN];

    if (!load(a, HASH_LEN))
        return 1;

    if (!fgets(buf, sizeof(buf), stdin))
        return 1;

    buf[strcspn(buf, "\r\n")] = 0;

    if (!compute(buf, b))
        return 1;

    if (memcmp(a, b, HASH_LEN) == 0)
        puts("OK");
    else
        puts("FAIL");

    return 0;
}