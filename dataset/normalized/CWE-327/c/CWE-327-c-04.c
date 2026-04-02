#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void open_message(void)
{
    FILE *source = NULL;
    HCRYPTPROV provider = 0;
    HCRYPTKEY cipher = 0;
    HCRYPTHASH digest = 0;
    char phrase[100];
    size_t phraseLen;
    char text[100];
    DWORD textLen = sizeof(text) - 1;

    printf("Password: ");
    if (fgets(phrase, sizeof(phrase), stdin) == NULL)
    {
        phrase[0] = '\0';
    }

    phraseLen = strlen(phrase);
    if (phraseLen > 0)
    {
        phrase[phraseLen - 1] = '\0';
    }

    source = fopen("encrypted.txt", "rb");
    if (source == NULL)
    {
        exit(1);
    }

    if (fread(text, sizeof(char), 100, source) != 100)
    {
        fclose(source);
        exit(1);
    }

    text[99] = '\0';

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
    {
        exit(1);
    }

    if (!CryptHashData(digest, (BYTE *)phrase, (DWORD)phraseLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(provider, CALG_3DES, digest, 0, &cipher))
    {
        exit(1);
    }

    if (!CryptDecrypt(cipher, 0, 1, 0, (BYTE *)text, &textLen))
    {
        exit(1);
    }

    text[textLen] = '\0';
    printf("%s\n", text);

    if (cipher)
    {
        CryptDestroyKey(cipher);
    }
    if (digest)
    {
        CryptDestroyHash(digest);
    }
    if (provider)
    {
        CryptReleaseContext(provider, 0);
    }
    if (source)
    {
        fclose(source);
    }
}

int main(void)
{
    open_message();
    return 0;
}