#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment (lib, "Advapi32")

static int process_buffer(const char *input)
{
    HCRYPTPROV provider = 0;
    HCRYPTHASH hash = 0;
    HCRYPTKEY key = 0;

    BYTE data[64];
    DWORD dataLen;
    char keyMaterial[64];

    strncpy((char *)data, input, sizeof(data) - 1);
    data[sizeof(data) - 1] = '\0';
    dataLen = (DWORD)strlen((char *)data);

    snprintf(keyMaterial, sizeof(keyMaterial), "session-%lu", GetCurrentProcessId());

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &hash))
    {
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (!CryptHashData(hash, (BYTE *)keyMaterial, (DWORD)strlen(keyMaterial), 0))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (!CryptDeriveKey(provider, CALG_AES_128, hash, 0, &key))
    {
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 0;
    }

    if (!CryptEncrypt(key, 0, TRUE, 0, data, &dataLen, sizeof(data)))
    {
        CryptDestroyKey(key);
        CryptDestroyHash(hash);
        CryptReleaseContext(provider, 0);
        return 0;
    }

    printf("Processed length: %lu\n", dataLen);

    CryptDestroyKey(key);
    CryptDestroyHash(hash);
    CryptReleaseContext(provider, 0);

    return 1;
}

int main(void)
{
    const char *msg = "example text";
    process_buffer(msg);
    return 0;
}
