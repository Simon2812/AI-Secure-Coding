#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define TEXT_SIZE 128
#define SUM_SIZE (512 / 8)

static int read_saved(UCHAR *buffer, size_t length)
{
    FILE *stream = fopen("secret.txt", "r");
    size_t i;

    if (stream == NULL)
    {
        return 0;
    }

    for (i = 0; i < length; i++)
    {
        ULONG value;
        if (fscanf(stream, "%02x", &value) != 1 || value > 0xff)
        {
            fclose(stream);
            return 0;
        }
        buffer[i] = (UCHAR)value;
    }

    fclose(stream);
    return 1;
}

static void trim_line(char *value)
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
    HCRYPTHASH digest = 0;
    char text[TEXT_SIZE];
    UCHAR saved[SUM_SIZE];
    UCHAR current[SUM_SIZE];
    DWORD currentSize = SUM_SIZE;

    if (!read_saved(saved, SUM_SIZE))
    {
        return 1;
    }

    if (fgets(text, sizeof(text), stdin) == NULL)
    {
        return 1;
    }

    trim_line(text);

    if (!CryptAcquireContextW(&context, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(context, CALG_SHA_512, 0, 0, &digest))
    {
        CryptReleaseContext(context, 0);
        return 1;
    }

    if (!CryptHashData(digest, (BYTE *)text, (DWORD)strlen(text), 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(context, 0);
        return 1;
    }

    if (!CryptGetHashParam(digest, HP_HASHVAL, current, &currentSize, 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(context, 0);
        return 1;
    }

    if (memcmp(saved, current, SUM_SIZE * sizeof(UCHAR)) == 0)
    {
        puts("Access granted");
    }
    else
    {
        puts("Access denied");
    }

    CryptDestroyHash(digest);
    CryptReleaseContext(context, 0);
    return 0;
}