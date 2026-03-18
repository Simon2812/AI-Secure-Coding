#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_CAPACITY 128
#define DIGEST_CAPACITY (256 / 8)

static int load_expected(UCHAR *buffer, size_t size)
{
    FILE *fp = fopen("password.txt", "r");
    size_t i;

    if (fp == NULL)
    {
        return 0;
    }

    for (i = 0; i < size; i++)
    {
        ULONG value;
        if (fscanf(fp, "%02x", &value) != 1 || value > 0xff)
        {
            fclose(fp);
            return 0;
        }
        buffer[i] = (UCHAR)value;
    }

    fclose(fp);
    return 1;
}

static void trim_newline(char *text)
{
    text[strcspn(text, "\r\n")] = '\0';
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    char input[INPUT_CAPACITY];
    UCHAR expected[DIGEST_CAPACITY];
    UCHAR actual[DIGEST_CAPACITY];
    DWORD actualSize = DIGEST_CAPACITY;

    if (!load_expected(expected, DIGEST_CAPACITY))
    {
        return 1;
    }

    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        return 1;
    }

    trim_newline(input);

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash))
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

    if (memcmp(expected, actual, DIGEST_CAPACITY) == 0)
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