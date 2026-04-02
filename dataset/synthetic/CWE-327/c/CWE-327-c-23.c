#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

static ALG_ID pick_cipher(int profile)
{
    if (profile == 0)
    {
        return CALG_AES_128;
    }

    return CALG_AES_256;
}

static int read_block(char *dst, DWORD *size)
{
    FILE *fp = fopen("encrypted.txt", "rb");
    if (fp == NULL)
    {
        return 0;
    }

    size_t count = fread(dst, 1, *size, fp);
    fclose(fp);

    if (count == 0)
    {
        return 0;
    }

    *size = (DWORD)count;
    return 1;
}

int main(void)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH digest = 0;
    HCRYPTKEY key = 0;

    char phrase[64];
    char content[128];
    DWORD contentLen = sizeof(content);
    ALG_ID cipher;
    int profile = 1;

    printf("Key: ");
    if (fgets(phrase, sizeof(phrase), stdin) == NULL)
    {
        return 1;
    }

    phrase[strcspn(phrase, "\n")] = '\0';

    if (!read_block(content, &contentLen))
    {
        return 1;
    }

    cipher = pick_cipher(profile);

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 1;
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        CryptReleaseContext(provider, 0);
        return 1;
    }

    if (!CryptHashData(digest, (BYTE *)phrase, (DWORD)strlen(phrase), 0))
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

    if (!CryptDecrypt(key, 0, TRUE, 0, (BYTE *)content, &contentLen))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(digest);
        CryptReleaseContext(provider, 0);
        return 1;
    }

    content[contentLen] = '\0';
    puts(content);

    CryptDestroyKey(key);
    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);

    return 0;
}