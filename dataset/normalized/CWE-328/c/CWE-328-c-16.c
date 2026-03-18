#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_LIMIT 128
#define DIGEST_SIZE (512 / 8)

static int read_hash(UCHAR *dst, size_t len)
{
    FILE *fp = fopen("password.txt", "r");
    size_t i;

    if (fp == NULL)
    {
        return 0;
    }

    for (i = 0; i < len; i++)
    {
        ULONG value;
        if (fscanf(fp, "%02x", &value) != 1 || value > 0xff)
        {
            fclose(fp);
            return 0;
        }
        dst[i] = (UCHAR)value;
    }

    fclose(fp);
    return 1;
}

static void chomp(char *text)
{
    char *p = strchr(text, '\r');
    if (p != NULL)
    {
        *p = '\0';
    }

    p = strchr(text, '\n');
    if (p != NULL)
    {
        *p = '\0';
    }
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    char input[INPUT_LIMIT];
    UCHAR expected[DIGEST_SIZE];
    UCHAR actual[DIGEST_SIZE];
    DWORD actualSize = DIGEST_SIZE;

    if (!read_hash(expected, DIGEST_SIZE))
    {
        return 1;
    }

    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        return 1;
    }

    chomp(input);

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_SHA_512, 0, 0, &hash))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(hash, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptGetHashParam(hash, HP_HASHVAL, actual, &actualSize, 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (memcmp(expected, actual, DIGEST_SIZE * sizeof(UCHAR)) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    return 0;
}