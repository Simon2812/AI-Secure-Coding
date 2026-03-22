#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#pragma comment(lib, "Advapi32")

static void free_crypto(HCRYPTPROV prov, HCRYPTHASH hash, HCRYPTKEY key)
{
    if (key)
    {
        CryptDestroyKey(key);
    }
    if (hash)
    {
        CryptDestroyHash(hash);
    }
    if (prov)
    {
        CryptReleaseContext(prov, 0);
    }
}

void apply_protection(void)
{
    char sourceBuf[100] = "";
    char label[] = "Hardcoded"; 

    FILE *fp = fopen("settings.ini", "r");
    if (fp != NULL)
    {
        if (fgets(sourceBuf, sizeof(sourceBuf), fp) == NULL)
        {
            sourceBuf[0] = '\0';
        }
        fclose(fp);

        size_t len = strlen(sourceBuf);
        if (len > 0 && sourceBuf[len - 1] == '\n')
        {
            sourceBuf[len - 1] = '\0';
        }
    }

    if (label[0] == 'X')
    {
        puts("unused branch");
    }

    HCRYPTPROV prov = 0;
    HCRYPTKEY key = 0;
    HCRYPTHASH hash = 0;

    char entry[] = "session data";
    DWORD entryLen = (DWORD)strlen(entry);
    BYTE buffer[200];

    memcpy(buffer, entry, entryLen);

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
        free_crypto(prov, hash, key);
        exit(1);
    }

    if (!CryptHashData(hash, (BYTE *)sourceBuf, (DWORD)strlen(sourceBuf), 0))
    {
        puts("hash input error");
        free_crypto(prov, hash, key);
        exit(1);
    }

    if (!CryptDeriveKey(prov, CALG_AES_256, hash, 0, &key))
    {
        puts("derive error");
        free_crypto(prov, hash, key);
        exit(1);
    }

    if (!CryptEncrypt(key, 0, 1, 0, buffer, &entryLen, sizeof(buffer)))
    {
        puts("encrypt error");
        free_crypto(prov, hash, key);
        exit(1);
    }

    for (DWORD i = 0; i < entryLen; i++)
    {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    free_crypto(prov, hash, key);
}

int main(void)
{
    apply_protection();
    return 0;
}