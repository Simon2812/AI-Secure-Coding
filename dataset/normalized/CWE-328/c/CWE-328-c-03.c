#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define BUF_SIZE 128
#define DIGEST_SIZE (128 / 8)

static int match_bytes(const UCHAR *x, const UCHAR *y, size_t n)
{
    return memcmp(x, y, n) == 0;
}

static int read_reference(UCHAR *out, size_t n)
{
    FILE *fp = fopen("password.txt", "r");
    size_t i;

    if (!fp)
    {
        return 0;
    }

    for (i = 0; i < n; i++)
    {
        ULONG v;
        if (fscanf(fp, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(fp);
            return 0;
        }
        out[i] = (UCHAR)v;
    }

    fclose(fp);
    return 1;
}

int main(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hsh = 0;
    char data[BUF_SIZE];
    UCHAR ref[DIGEST_SIZE];
    UCHAR out[DIGEST_SIZE];
    DWORD len = DIGEST_SIZE;
    char *q;

    if (!read_reference(ref, DIGEST_SIZE))
    {
        return 1;
    }

    if (!fgets(data, sizeof(data), stdin))
    {
        return 1;
    }

    q = strchr(data, '\r');
    if (q) *q = '\0';
    q = strchr(data, '\n');
    if (q) *q = '\0';

    if (!CryptAcquireContextW(&prov, NULL, NULL, PROV_RSA_FULL, 0))
    {
        return 1;
    }

    if (!CryptCreateHash(prov, CALG_SHA1, 0, 0, &hsh))
    {
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptHashData(hsh, (BYTE *)data, (DWORD)strlen(data), 0))
    {
        CryptDestroyHash(hsh);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    if (!CryptGetHashParam(hsh, HP_HASHVAL, (BYTE *)out, &len, 0))
    {
        CryptDestroyHash(hsh);
        CryptReleaseContext(prov, 0);
        return 1;
    }

    puts(match_bytes(ref, out, DIGEST_SIZE * sizeof(UCHAR)) ? "Access granted" : "Access denied");

    CryptDestroyHash(hsh);
    CryptReleaseContext(prov, 0);
    return 0;
}