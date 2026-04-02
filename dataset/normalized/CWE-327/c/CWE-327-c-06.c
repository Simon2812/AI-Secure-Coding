#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static void reveal_text(void)
{
    FILE *inputFile = NULL;
    HCRYPTPROV crypto = 0;
    HCRYPTKEY activeKey = 0;
    HCRYPTHASH passwordHash = 0;
    char secretText[100];
    size_t secretLen;
    char payload[100];
    DWORD payloadLen = sizeof(payload) - 1;

    printf("Password: ");
    if (fgets(secretText, sizeof(secretText), stdin) == NULL)
    {
        secretText[0] = '\0';
    }

    secretLen = strlen(secretText);
    if (secretLen > 0)
    {
        secretText[secretLen - 1] = '\0';
    }

    inputFile = fopen("encrypted.txt", "rb");
    if (inputFile == NULL)
    {
        exit(1);
    }

    if (fread(payload, sizeof(char), 100, inputFile) != 100)
    {
        fclose(inputFile);
        exit(1);
    }

    payload[99] = '\0';

    if (!CryptAcquireContext(&crypto, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&crypto, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            exit(1);
        }
    }

    if (!CryptCreateHash(crypto, CALG_SHA_256, 0, 0, &passwordHash))
    {
        exit(1);
    }

    if (!CryptHashData(passwordHash, (BYTE *)secretText, (DWORD)secretLen, 0))
    {
        exit(1);
    }

    if (!CryptDeriveKey(crypto, CALG_RC5, passwordHash, 0, &activeKey))
    {
        exit(1);
    }

    if (!CryptDecrypt(activeKey, 0, 1, 0, (BYTE *)payload, &payloadLen))
    {
        exit(1);
    }

    payload[payloadLen] = '\0';
    printf("%s\n", payload);

    if (activeKey)
    {
        CryptDestroyKey(activeKey);
    }
    if (passwordHash)
    {
        CryptDestroyHash(passwordHash);
    }
    if (crypto)
    {
        CryptReleaseContext(crypto, 0);
    }
    if (inputFile)
    {
        fclose(inputFile);
    }
}

int main(void)
{
    reveal_text();
    return 0;
}