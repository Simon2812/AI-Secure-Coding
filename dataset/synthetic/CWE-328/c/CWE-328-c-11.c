#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define BUF_SIZE 128
#define HASH_FULL 32
#define HASH_PART 8

static int load_hash(UCHAR *dst, size_t n)
{
    FILE *fp = fopen("password.txt", "r");
    size_t i;

    if (!fp)
    {
        return 0;
    }

    for (i = 0; i < n; i++)
    {
        ULONG tmp;
        if (fscanf(fp, "%02x", &tmp) != 1 || tmp > 0xff)
        {
            fclose(fp);
            return 0;
        }
        dst[i] = (UCHAR)tmp;
    }

    fclose(fp);
    return 1;
}

static int verify(const char *input, const UCHAR *ref)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hash = 0;
    UCHAR out[HASH_FULL];
    DWORD outLen = HASH_FULL;
    int result = 0;

    if (!CryptAcquireContextW(&prov, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 0;
    }

    if (!CryptCreateHash(prov, CALG_SHA_256, 0, 0, &hash))
    {
        CryptReleaseContext(prov, 0);
        return 0;
    }

    if (!CryptHashData(hash, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(prov, 0);
        return 0;
    }

    if (CryptGetHashParam(hash, HP_HASHVAL, out, &outLen, 0))
    {
        if (memcmp(ref, out, HASH_PART) == 0)
        {
            result = 1;
        }
    }

    CryptDestroyHash(hash);
    CryptReleaseContext(prov, 0);
    return result;
}

int main(void)
{
    char buf[BUF_SIZE];
    UCHAR expected[HASH_FULL];

    if (!load_hash(expected, HASH_FULL))
    {
        return 1;
    }

    if (!fgets(buf, sizeof(buf), stdin))
    {
        return 1;
    }

    buf[strcspn(buf, "\r\n")] = '\0';

    if (verify(buf, expected))
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    return 0;
}