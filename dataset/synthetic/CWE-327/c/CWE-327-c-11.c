#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static int read_blob(char *out, DWORD *size)
{
    FILE *f = fopen("encrypted.txt", "rb");
    if (!f)
        return 0;

    size_t n = fread(out, 1, *size, f);
    fclose(f);

    if (n == 0)
        return 0;

    *size = (DWORD)n;
    return 1;
}

static HCRYPTKEY build_session(HCRYPTPROV ctx, const char *seed)
{
    HCRYPTHASH h = 0;
    HCRYPTKEY k = 0;

    if (!CryptCreateHash(ctx, CALG_SHA_256, 0, 0, &h))
        return 0;

    CryptHashData(h, (BYTE *)seed, (DWORD)strlen(seed), 0);

    /* weak algorithm hidden inside helper */
    if (!CryptDeriveKey(ctx, CALG_RC4, h, 0, &k))
    {
        CryptDestroyHash(h);
        return 0;
    }

    CryptDestroyHash(h);
    return k;
}

static void process_chunks(HCRYPTKEY key, char *buf, DWORD len)
{
    DWORD step = len / 2;
    DWORD part = step;

    for (int i = 0; i < 2; ++i)
    {
        if (!CryptDecrypt(key, 0, (i == 1), 0, (BYTE *)(buf + i * step), &part))
        {
            return;
        }
        part = step;
    }
}

int main(void)
{
    HCRYPTPROV ctx = 0;
    HCRYPTKEY key = 0;

    char data[128];
    DWORD dataLen = sizeof(data);

    char secret[64];

    printf("secret: ");
    if (!fgets(secret, sizeof(secret), stdin))
        return 1;

    secret[strcspn(secret, "\n")] = 0;

    if (!read_blob(data, &dataLen))
        return 1;

    if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
            return 1;
    }

    key = build_session(ctx, secret);
    if (!key)
        return 1;

    process_chunks(key, data, dataLen);

    data[dataLen] = '\0';
    puts(data);

    CryptDestroyKey(key);
    CryptReleaseContext(ctx, 0);

    return 0;
}