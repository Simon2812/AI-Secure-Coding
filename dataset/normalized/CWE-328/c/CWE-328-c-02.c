#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_SIZE 128
#define HASH_LEN (128 / 8)

static int verify(const UCHAR *a, const UCHAR *b, size_t len)
{
    return memcmp(a, b, len) == 0;
}

int main(void)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;
    FILE *f = NULL;
    char buf[INPUT_SIZE];
    UCHAR stored[HASH_LEN];
    UCHAR produced[HASH_LEN];
    DWORD outLen = HASH_LEN;
    char *p;
    size_t k;

    f = fopen("password.txt", "r");
    if (!f)
    {
        return 1;
    }

    for (k = 0; k < HASH_LEN; k++)
    {
        ULONG tmp;
        if (fscanf(f, "%02x", &tmp) != 1)
        {
            fclose(f);
            return 1;
        }
        if (tmp > 0xff)
        {
            fclose(f);
            return 1;
        }
        stored[k] = (UCHAR)tmp;
    }

    fclose(f);

    if (!fgets(buf, sizeof(buf), stdin))
    {
        return 1;
    }

    p = strchr(buf, '\r');
    if (p) *p = '\0';
    p = strchr(buf, '\n');
    if (p) *p = '\0';

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(ctx, CALG_MD5, 0, 0, &h))
    {
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (!CryptHashData(h, (BYTE *)buf, (DWORD)strlen(buf), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (!CryptGetHashParam(h, HP_HASHVAL, (BYTE *)produced, &outLen, 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    puts(verify(stored, produced, HASH_LEN * sizeof(UCHAR)) ? "Access granted" : "Access denied");

    CryptDestroyHash(h);
    CryptReleaseContext(ctx, 0);
    return 0;
}