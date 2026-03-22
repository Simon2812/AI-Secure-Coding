#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

void handle(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char text[] = "String to be encrypted";
    BYTE buf[200];
    DWORD len = (DWORD)strlen(text);

    char material[100] = "";
    int mode = 2;

    switch (mode)
    {
        case 1:
            strcpy(material, "Alpha");
            break;
        case 2:
            strcpy(material, "BetaValue");
            break;
        default:
            material[0] = '\0';
            break;
    }

    memcpy(buf, text, len);

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

    if (!CryptEncrypt(key, 0, 1, 0, buf, &len, sizeof(buf)))
    {
        puts("encrypt error");
        exit(1);
    }

    for (DWORD i = 0; i < len; i++)
    {
        printf("%02X", buf[i]);
    }
    printf("\n");

    if (key) CryptDestroyKey(key);
    if (hash) CryptDestroyHash(hash);
    if (prov) CryptReleaseContext(prov, 0);
}

int main(void)
{
    handle();
    return 0;
}