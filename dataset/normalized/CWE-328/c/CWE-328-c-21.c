#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_BUFFER 128
#define OUTPUT_BYTES (256 / 8)

static int load_digest(UCHAR *target, size_t count)
{
    FILE *file = fopen("password.txt", "r");
    size_t i;

    if (file == NULL)
    {
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        ULONG value;
        if (fscanf(file, "%02x", &value) != 1 || value > 0xff)
        {
            fclose(file);
            return 0;
        }
        target[i] = (UCHAR)value;
    }

    fclose(file);
    return 1;
}

static void sanitize(char *buffer)
{
    char *mark = strchr(buffer, '\r');
    if (mark != NULL)
    {
        *mark = '\0';
    }

    mark = strchr(buffer, '\n');
    if (mark != NULL)
    {
        *mark = '\0';
    }
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hashHandle = 0;
    char password[INPUT_BUFFER];
    UCHAR stored[OUTPUT_BYTES];
    UCHAR computed[OUTPUT_BYTES];
    DWORD length = OUTPUT_BYTES;

    if (!load_digest(stored, OUTPUT_BYTES))
    {
        return 1;
    }

    if (fgets(password, sizeof(password), stdin) == NULL)
    {
        return 1;
    }

    sanitize(password);

    if (!CryptAcquireContextW(&provider, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hashHandle))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(hashHandle, (BYTE *)password, (DWORD)strlen(password), 0))
    {
        CryptDestroyHash(hashHandle);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptGetHashParam(hashHandle, HP_HASHVAL, computed, &length, 0))
    {
        CryptDestroyHash(hashHandle);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (memcmp(stored, computed, OUTPUT_BYTES) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    CryptDestroyHash(hashHandle);
    CryptReleaseContext(provider, 0);
    return 0;
}
