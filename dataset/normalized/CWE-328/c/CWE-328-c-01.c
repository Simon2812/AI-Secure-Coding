#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_LIMIT 128
#define DIGEST_BYTES (128 / 8)

static void print_status(int granted)
{
    if (granted)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    FILE *stream = NULL;
    char input[INPUT_LIMIT];
    UCHAR expected[DIGEST_BYTES];
    UCHAR actual[DIGEST_BYTES];
    DWORD actualSize = DIGEST_BYTES;
    char *newline = NULL;
    size_t index;

    stream = fopen("password.txt", "r");
    if (stream == NULL)
    {
        return 1;
    }

    for (index = 0; index < DIGEST_BYTES; index++)
    {
        ULONG part;
        if (fscanf(stream, "%02x", &part) != 1)
        {
            fclose(stream);
            return 1;
        }
        if (part > 0xff)
        {
            fclose(stream);
            return 1;
        }
        expected[index] = (UCHAR)part;
    }

    fclose(stream);

    if (fgets(input, sizeof(input), stdin) == NULL)
    {
        return 1;
    }

    newline = strchr(input, '\r');
    if (newline != NULL)
    {
        *newline = '\0';
    }

    newline = strchr(input, '\n');
    if (newline != NULL)
    {
        *newline = '\0';
    }

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_MD2, 0, 0, &hash))
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

    if (!CryptGetHashParam(hash, HP_HASHVAL, (BYTE *)actual, &actualSize, 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    print_status(memcmp(expected, actual, DIGEST_BYTES * sizeof(UCHAR)) == 0);

    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);
    return 0;
}