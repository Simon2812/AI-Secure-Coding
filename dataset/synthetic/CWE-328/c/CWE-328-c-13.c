#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define LIMIT 128
#define SIZE 16

static int load(UCHAR *buf, size_t n)
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
        buf[i] = (UCHAR)v;
    }

    fclose(f);
    return 1;
}

static int process(const char *text, UCHAR *out)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    DWORD len = SIZE;
    int ok = 0;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 0;

    ALG_ID alg = (strlen(text) < 8) ? CALG_MD5 : CALG_SHA1;

    if (!CryptCreateHash(ctx, alg, 0, 0, &h))
    {
        CryptReleaseContext(ctx, 0);
        return 0;
    }

    if (!CryptHashData(h, (BYTE *)text, (DWORD)strlen(text), 0))
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
    char buf[LIMIT];
    UCHAR ref[SIZE];
    UCHAR out[SIZE];

    if (!load(ref, SIZE))
        return 1;

    if (!fgets(buf, sizeof(buf), stdin))
        return 1;

    buf[strcspn(buf, "\r\n")] = '\0';

    if (!process(buf, out))
        return 1;

    if (memcmp(ref, out, SIZE) == 0)
        puts("Access granted");
    else
        puts("Access denied");

    return 0;
}