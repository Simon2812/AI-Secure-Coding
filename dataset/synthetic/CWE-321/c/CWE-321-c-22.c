#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void destroy_crypto(HCRYPTPROV provider, HCRYPTHASH digest, HCRYPTKEY derived)
{
    if (derived)
    {
        CryptDestroyKey(derived);
    }
    if (digest)
    {
        CryptDestroyHash(digest);
    }
    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
}

int main(int argc, char *argv[])
{
    char phrase[100] = "";

    if (argc > 1)
    {
        strncpy(phrase, argv[1], sizeof(phrase) - 1);
        phrase[sizeof(phrase) - 1] = '\0';
    }

    HCRYPTPROV provider = 0;
    HCRYPTKEY derived = 0;
    HCRYPTHASH digest = 0;

    char note[] = "backup record";
    DWORD noteLen = (DWORD)strlen(note);
    BYTE bytes[200];

    memcpy(bytes, note, noteLen);

    if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("acquire error");
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        puts("hash error");
        destroy_crypto(provider, digest, derived);
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)phrase, (DWORD)strlen(phrase), 0))
    {
        puts("hash input error");
        destroy_crypto(provider, digest, derived);
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_AES_256, digest, 0, &derived))
    {
        puts("derive error");
        destroy_crypto(provider, digest, derived);
        exit(1);
    }

    if (!CryptEncrypt(derived, 0, 1, 0, bytes, &noteLen, sizeof(bytes)))
    {
        puts("encrypt error");
        destroy_crypto(provider, digest, derived);
        exit(1);
    }

    for (DWORD i = 0; i < noteLen; i++)
    {
        printf("%02X", bytes[i]);
    }
    printf("\n");

    destroy_crypto(provider, digest, derived);
    return 0;
}