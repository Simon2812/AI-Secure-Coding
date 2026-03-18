#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define N 128
#define HLEN (512 / 8)

typedef struct {
    UCHAR stored[HLEN];
    UCHAR computed[HLEN];
} block;

static int equal(const UCHAR *a, const UCHAR *b)
{
    size_t i;
    unsigned char diff = 0;

    for (i = 0; i < HLEN; i++)
    {
        diff |= a[i] ^ b[i];
    }

    return diff == 0;
}

int main(void)
{
    FILE *f = fopen("password.txt", "r");
    block b;
    char input[N];
    size_t i;
    DWORD size = HLEN;
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h = 0;

    if (!f) return 1;

    for (i = 0; i < HLEN; i++)
    {
        ULONG v;
        if (fscanf(f, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(f);
            return 1;
        }
        b.stored[i] = (UCHAR)v;
    }
    fclose(f);

    if (!fgets(input, sizeof(input), stdin))
        return 1;

    input[strcspn(input, "\n")] = 0;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(ctx, CALG_SHA_512, 0, 0, &h))
    {
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    CryptHashData(h, (BYTE*)input, (DWORD)strlen(input), 0);
    CryptGetHashParam(h, HP_HASHVAL, b.computed, &size, 0);

    puts(equal(b.stored, b.computed) ? "OK" : "FAIL");

    CryptDestroyHash(h);
    CryptReleaseContext(ctx, 0);
    return 0;
}
