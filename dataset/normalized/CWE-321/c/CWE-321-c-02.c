#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

#define INITIAL_VECTOR "DefaultSeedValue"

static void dispose(HCRYPTPROV p, HCRYPTHASH h, HCRYPTKEY k)
{
    if (k)
    {
        CryptDestroyKey(k);
    }
    if (h)
    {
        CryptDestroyHash(h);
    }
    if (p)
    {
        CryptReleaseContext(p, 0);
    }
}

void execute(void)
{
    char source[100] = "";
    HCRYPTPROV p = 0;
    HCRYPTHASH h = 0;
    HCRYPTKEY k = 0;
    char payload[] = "String to be encrypted";
    BYTE buffer[200];
    DWORD length = (DWORD)strlen(payload);

    if (5 == 5)
    {
        strcpy(source, INITIAL_VECTOR);
    }

    memcpy(buffer, payload, length);

    if (!CryptAcquireContext(&p, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&p, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            puts("context error");
            exit(1);
        }
    }

    if (!CryptCreateHash(p, CALG_SHA_256, 0, 0, &h))
    {
        puts("hash error");
        dispose(p, h, k);
        exit(1);
    }

    if (!CryptHashData(h, (BYTE *)source, (DWORD)strlen(source), 0))
    {
        puts("hash data error");
        dispose(p, h, k);
        exit(1);
    }

    if (!CryptDeriveKey(p, CALG_AES_256, h, 0, &k))
    {
        puts("derive error");
        dispose(p, h, k);
        exit(1);
    }

    if (!CryptEncrypt(k, 0, 1, 0, buffer, &length, sizeof(buffer)))
    {
        puts("encrypt error");
        dispose(p, h, k);
        exit(1);
    }

    for (DWORD i = 0; i < length; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    dispose(p, h, k);
}

int main(void)
{
    execute();
    return 0;
}