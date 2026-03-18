#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define BUFFER_LIMIT 128
#define HASH_LENGTH (512 / 8)

static int load_value(UCHAR *out, size_t count)
{
    FILE *file = fopen("password.txt", "r");
    size_t i;

    if (file == NULL)
    {
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        ULONG part;
        if (fscanf(file, "%02x", &part) != 1 || part > 0xff)
        {
            fclose(file);
            return 0;
        }
        out[i] = (UCHAR)part;
    }

    fclose(file);
    return 1;
}

static void trim_input(char *text)
{
    char *pos = strchr(text, '\r');
    if (pos != NULL)
    {
        *pos = '\0';
    }

    pos = strchr(text, '\n');
    if (pos != NULL)
    {
        *pos = '\0';
    }
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH state = 0;
    char secret[BUFFER_LIMIT];
    UCHAR left[HASH_LENGTH];
    UCHAR right[HASH_LENGTH];
    DWORD size = HASH_LENGTH;

    if (!load_value(left, HASH_LENGTH))
    {
        return 1;
    }

    if (fgets(secret, sizeof(secret), stdin) == NULL)
    {
        return 1;
    }

    trim_input(secret);

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_SHA_512, 0, 0, &state))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(state, (BYTE *)secret, (DWORD)strlen(secret), 0))
    {
        CryptDestroyHash(state);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptGetHashParam(state, HP_HASHVAL, right, &size, 0))
    {
        CryptDestroyHash(state);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (memcmp(left, right, HASH_LENGTH * sizeof(UCHAR)) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    CryptDestroyHash(state);
    CryptReleaseContext(provider, 0);
    return 0;
}