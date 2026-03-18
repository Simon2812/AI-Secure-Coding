#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define MAX_LEN 128
#define SIZE16 (128 / 8)

static int read_bytes(UCHAR *buf, size_t count)
{
    FILE *file = fopen("password.txt", "r");
    size_t j;

    if (!file)
        return 0;

    for (j = 0; j < count; j++)
    {
        ULONG num;
        if (fscanf(file, "%02x", &num) != 1 || num > 0xff)
        {
            fclose(file);
            return 0;
        }
        buf[j] = (UCHAR)num;
    }

    fclose(file);
    return 1;
}

static void trim_line(char *s)
{
    char *c = strchr(s, '\r');
    if (c) *c = '\0';
    c = strchr(s, '\n');
    if (c) *c = '\0';
}

int main(void)
{
    HCRYPTPROV handle = 0;
    HCRYPTHASH hashObj = 0;
    char line[MAX_LEN];
    UCHAR reference[SIZE16];
    UCHAR result[SIZE16];
    DWORD len = SIZE16;

    if (!read_bytes(reference, SIZE16))
        return 1;

    if (!fgets(line, sizeof(line), stdin))
        return 1;

    trim_line(line);

    if (!CryptAcquireContextW(&handle, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(handle, CALG_MD5, 0, 0, &hashObj))
    {
        CryptReleaseContext(handle, 0);
        return 1;
    }

    if (!CryptHashData(hashObj, (BYTE *)line, (DWORD)strlen(line), 0))
    {
        CryptDestroyHash(hashObj);
        CryptReleaseContext(handle, 0);
        return 1;
    }

    if (!CryptGetHashParam(hashObj, HP_HASHVAL, (BYTE *)result, &len, 0))
    {
        CryptDestroyHash(hashObj);
        CryptReleaseContext(handle, 0);
        return 1;
    }

    puts(memcmp(reference, result, SIZE16 * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(hashObj);
    CryptReleaseContext(handle, 0);
    return 0;
}