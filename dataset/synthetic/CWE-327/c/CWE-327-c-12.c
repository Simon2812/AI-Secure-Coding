#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

static ALG_ID select_algo(int mode)
{
    if (mode == 1)
        return CALG_RC4;

    return CALG_AES_256;
}

int main(void)
{
    HCRYPTPROV prov = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    char keyMaterial[64];
    char content[128];
    DWORD contentLen = sizeof(content);

    FILE *fp = fopen("encrypted.txt", "rb");
    if (!fp)
        return 1;

    fread(content, 1, sizeof(content), fp);
    fclose(fp);

    printf("input: ");
    if (!fgets(keyMaterial, sizeof(keyMaterial), stdin))
        return 1;

    keyMaterial[strcspn(keyMaterial, "\n")] = 0;

    if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&prov, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
            return 1;
    }

    if (!CryptCreateHash(prov, CALG_SHA_256, 0, 0, &hash))
        return 1;

    CryptHashData(hash, (BYTE *)keyMaterial, (DWORD)strlen(keyMaterial), 0);

    int mode = 1; /* runtime choice */

    ALG_ID chosen = select_algo(mode);

    if (!CryptDeriveKey(prov, chosen, hash, 0, &key))
        return 1;

    if (!CryptDecrypt(key, 0, 1, 0, (BYTE *)content, &contentLen))
        return 1;

    content[contentLen] = '\0';
    puts(content);

    CryptDestroyKey(key);
    CryptDestroyHash(hash);
    CryptReleaseContext(prov, 0);

    return 0;
}