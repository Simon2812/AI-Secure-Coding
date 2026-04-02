#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

static int load_file(char *buf, DWORD *len)
{
    FILE *f = fopen("encrypted.txt", "rb");
    if (!f)
        return 0;

    size_t n = fread(buf, 1, *len, f);
    fclose(f);

    if (n == 0)
        return 0;

    *len = (DWORD)n;
    return 1;
}

static int init_crypto(HCRYPTPROV *ctx, HCRYPTHASH *digest, const char *secret)
{
    if (!CryptAcquireContext(ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(ctx, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
            return 0;
    }

    if (!CryptCreateHash(*ctx, CALG_SHA_256, 0, 0, digest))
        return 0;

    if (!CryptHashData(*digest, (BYTE *)secret, (DWORD)strlen(secret), 0))
        return 0;

    return 1;
}

static HCRYPTKEY derive_cipher(HCRYPTPROV ctx, HCRYPTHASH digest)
{
    HCRYPTKEY key = 0;

    if (!CryptDeriveKey(ctx, CALG_3DES, digest, 0, &key))
        return 0;

    return key;
}

int main(void)
{
    char secret[64];
    char data[128];
    DWORD dataLen = sizeof(data);

    HCRYPTPROV ctx = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;

    printf("Enter secret: ");
    if (!fgets(secret, sizeof(secret), stdin))
        return 1;

    secret[strcspn(secret, "\n")] = 0;

    if (!load_file(data, &dataLen))
        return 1;

    if (!init_crypto(&ctx, &digest, secret))
        return 1;

    key = derive_cipher(ctx, digest);
    if (!key)
        return 1;

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)data, &dataLen))
        return 1;

    data[dataLen] = '\0';
    puts(data);

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(ctx, 0);

    return 0;
}