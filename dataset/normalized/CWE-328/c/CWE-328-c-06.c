#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define INPUT_CAP 128
#define HASH_PART (128 / 8)

static int load_expected(UCHAR *buf, size_t n)
{
    FILE *fd = fopen("password.txt", "r");
    size_t i;

    if (!fd)
        return 0;

    for (i = 0; i < n; i++)
    {
        ULONG v;
        if (fscanf(fd, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(fd);
            return 0;
        }
        buf[i] = (UCHAR)v;
    }

    fclose(fd);
    return 1;
}

static void clean(char *s)
{
    char *p = strchr(s, '\r');
    if (p) *p = '\0';
    p = strchr(s, '\n');
    if (p) *p = '\0';
}

int main(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hnd = 0;
    char input[INPUT_CAP];
    UCHAR expected[HASH_PART];
    UCHAR computed[HASH_PART];
    DWORD outSize = HASH_PART;

    if (!load_expected(expected, HASH_PART))
        return 1;

    if (!fgets(input, sizeof(input), stdin))
        return 1;

    clean(input);

    if (!CryptAcquireContextW(&prov, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(prov, CALG_SHA1, 0, 0, &hnd))
    {
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptHashData(hnd, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(hnd);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptGetHashParam(hnd, HP_HASHVAL, (BYTE *)computed, &outSize, 0))
    {
        CryptDestroyHash(hnd);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    puts(memcmp(expected, computed, HASH_PART * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(hnd);
    CryptReleaseContext(prov, 0);
    return 0;
}