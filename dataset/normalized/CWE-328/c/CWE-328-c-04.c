#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define LIMIT 128
#define BLOCK (128 / 8)

static int load_hash(UCHAR *dst, size_t n)
{
    FILE *in = fopen("password.txt", "r");
    size_t i;

    if (!in)
        return 0;

    for (i = 0; i < n; i++)
    {
        ULONG x;
        if (fscanf(in, "%02x", &x) != 1 || x > 0xff)
        {
            fclose(in);
            return 0;
        }
        dst[i] = (UCHAR)x;
    }

    fclose(in);
    return 1;
}

static void strip(char *s)
{
    char *t = strchr(s, '\r');
    if (t) *t = '\0';
    t = strchr(s, '\n');
    if (t) *t = '\0';
}

int main(void)
{
    HCRYPTPROV c = 0;
    HCRYPTHASH h = 0;
    char input[LIMIT];
    UCHAR ref[BLOCK];
    UCHAR out[BLOCK];
    DWORD sz = BLOCK;

    if (!load_hash(ref, BLOCK))
        return 1;

    if (!fgets(input, sizeof(input), stdin))
        return 1;

    strip(input);

    if (!CryptAcquireContextW(&c, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(c, CALG_MD2, 0, 0, &h))
    {
        CryptReleaseContext(c, 0);
        return 1;
    }

    if (!CryptHashData(h, (BYTE *)input, (DWORD)strlen(input), 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(c, 0);
        return 1;
    }

    if (!CryptGetHashParam(h, HP_HASHVAL, (BYTE *)out, &sz, 0))
    {
        CryptDestroyHash(h);
        CryptReleaseContext(c, 0);
        return 1;
    }

    puts(memcmp(ref, out, BLOCK * sizeof(UCHAR)) == 0 ? "Access granted" : "Access denied");

    CryptDestroyHash(h);
    CryptReleaseContext(c, 0);
    return 0;
}