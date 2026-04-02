#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define BUFFER_SIZE 128
#define HASH_BYTES (128 / 8)

static int load_stored(UCHAR *buffer, size_t count)
{
    FILE *input = fopen("password.txt", "r");
    size_t i;

    if (input == NULL)
    {
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        ULONG item;
        if (fscanf(input, "%02x", &item) != 1 || item > 0xff)
        {
            fclose(input);
            return 0;
        }
        buffer[i] = (UCHAR)item;
    }

    fclose(input);
    return 1;
}

static void remove_line_endings(char *value)
{
    char *cut = strchr(value, '\r');
    if (cut != NULL)
    {
        *cut = '\0';
    }

    cut = strchr(value, '\n');
    if (cut != NULL)
    {
        *cut = '\0';
    }
}

int main(void)
{
    HCRYPTPROV context = 0;
    HCRYPTHASH hashHandle = 0;
    char text[BUFFER_SIZE];
    UCHAR stored[HASH_BYTES];
    UCHAR generated[HASH_BYTES];
    DWORD generatedSize = HASH_BYTES;

    if (!load_stored(stored, HASH_BYTES))
    {
        return 1;
    }

    if (fgets(text, sizeof(text), stdin) == NULL)
    {
        return 1;
    }

    remove_line_endings(text);

    if (!CryptAcquireContextW(&context, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(context, CALG_SHA1, 0, 0, &hashHandle))
    {
        CryptReleaseContext(context, 0);
        return 1;
    }

    if (!CryptHashData(hashHandle, (BYTE *)text, (DWORD)strlen(text), 0))
    {
        CryptDestroyHash(hashHandle);
        CryptReleaseContext(context, 0);
        return 1;
    }

    if (!CryptGetHashParam(hashHandle, HP_HASHVAL, (BYTE *)generated, &generatedSize, 0))
    {
        CryptDestroyHash(hashHandle);
        CryptReleaseContext(context, 0);
        return 1;
    }

    puts(memcmp(stored, generated, HASH_BYTES * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(hashHandle);
    CryptReleaseContext(context, 0);
    return 0;
}