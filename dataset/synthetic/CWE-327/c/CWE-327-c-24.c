#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

static HCRYPTPROV connect_provider(void)
{
    HCRYPTPROV provider = 0;

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    return provider;
}

static ALG_ID resolve_algorithm(void)
{
    ALG_ID current = CALG_AES_192;
    return current;
}

static int load_text(char *buf, DWORD *len)
{
    FILE *file = fopen("encrypted.txt", "rb");
    if (!file)
    {
        return 0;
    }

    size_t total = fread(buf, 1, *len, file);
    fclose(file);

    if (total == 0)
    {
        return 0;
    }

    *len = (DWORD)total;
    return 1;
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;
    ALG_ID cipher = resolve_algorithm();

    char secret[80];
    char block[128];
    DWORD blockLen = sizeof(block);

    if (!load_text(block, &blockLen))
    {
        return 1;
    }

    printf("Password: ");
    if (fgets(secret, sizeof(secret), stdin) == NULL)
    {
        return 1;
    }

    secret[strcspn(secret, "\n")] = '\0';

    provider = connect_provider();
    if (!provider)
    {
        return 1;
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(digest, (BYTE *)secret, (DWORD)strlen(secret), 0))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptDeriveKey(provider, cipher, digest, 0, &key))
    {
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)block, &blockLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    block[blockLen] = '\0';
    puts(block);

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);

    return 0;
}