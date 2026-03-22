#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

void run_task(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char payload[] = "String to be encrypted";
    BYTE buffer[200];
    DWORD bufferLen = (DWORD)strlen(payload);

    char material[100];

    if (bufferLen > 0)
    {
        strcpy(material, "SessionValue");
    }
    else
    {
        material[0] = '\0';
    }

    memcpy(buffer, payload, bufferLen);

    if (!CryptAcquireContext(&prov, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&prov, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(prov, CALG_SHA_256, 0, 0, &hash))
    {
        puts("hash error");
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)material, (DWORD)strlen(material), 0))
    {
        puts("hash data error");
        exit(1);
    }

    if (!CryptDeriveKey(prov, CALG_AES_256, hash, 0, &key))
    {
        puts("derive error");
        exit(1);
    }

    if (!CryptEncrypt(key, 0, 1, 0, buffer, &bufferLen, sizeof(buffer)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < bufferLen; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    if (key) CryptDestroyKey(key);
    if (hash) CryptDestroyHash(hash);
    if (prov) CryptReleaseContext(prov, 0);
}

int main(void)
{
    run_task();
    return 0;
}