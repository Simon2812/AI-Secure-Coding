#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define LINE_LIMIT 128
#define DIGEST_WIDTH (128 / 8)

static int read_expected_hash(UCHAR *data, size_t size)
{
    FILE *handle = fopen("password.txt", "r");
    size_t idx;

    if (handle == NULL)
    {
        return 0;
    }

    for (idx = 0; idx < size; idx++)
    {
        ULONG value;
        if (fscanf(handle, "%02x", &value) != 1 || value > 0xff)
        {
            fclose(handle);
            return 0;
        }
        data[idx] = (UCHAR)value;
    }

    fclose(handle);
    return 1;
}

static void normalize_input(char *text)
{
    char *end = strchr(text, '\r');
    if (end != NULL)
    {
        *end = '\0';
    }

    end = strchr(text, '\n');
    if (end != NULL)
    {
        *end = '\0';
    }
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    char password[LINE_LIMIT];
    UCHAR known[DIGEST_WIDTH];
    UCHAR candidate[DIGEST_WIDTH];
    DWORD length = DIGEST_WIDTH;

    if (!read_expected_hash(known, DIGEST_WIDTH))
    {
        return 1;
    }

    if (fgets(password, sizeof(password), stdin) == NULL)
    {
        return 1;
    }

    normalize_input(password);

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_MD5, 0, 0, &hash))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(hash, (BYTE *)password, (DWORD)strlen(password), 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptGetHashParam(hash, HP_HASHVAL, (BYTE *)candidate, &length, 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    puts(memcmp(known, candidate, DIGEST_WIDTH * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    return 0;
}