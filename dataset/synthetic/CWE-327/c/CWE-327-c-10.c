#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#pragma comment (lib, "Advapi32")

static HCRYPTPROV init_provider(void)
{
    HCRYPTPROV provider = 0;

    if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, 0))
    {
        if (!CryptAcquireContext(&provider, NULL, MS_ENH_RSA_AES_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
        {
            return 0;
        }
    }

    return provider;
}

static HCRYPTHASH build_digest(HCRYPTPROV provider, const char *secret)
{
    HCRYPTHASH digest = 0;

    if (!CryptCreateHash(provider, CALG_SHA_256, 0, 0, &digest))
        return 0;

    CryptHashData(digest, (BYTE *)secret, (DWORD)strlen(secret), 0);

    return digest;
}

static int unlock_payload(HCRYPTPROV provider, HCRYPTHASH digest, char *data, DWORD *size)
{
    HCRYPTKEY sessionA = 0;
    HCRYPTKEY sessionB = 0;

    /* weak usage #1 */
    if (!CryptDeriveKey(provider, CALG_RC2, digest, 0, &sessionA))
        return 0;

    /* weak usage #2 */
    if (!CryptDeriveKey(provider, CALG_RC2, digest, 0, &sessionB))
        return 0;

    if (!CryptDecrypt(sessionA, 0, TRUE, 0, (BYTE *)data, size))
        return 0;

    CryptDestroyKey(sessionA);
    CryptDestroyKey(sessionB);

    return 1;
}

int main(void)
{
    char secret[64];
    char payload[128];
    DWORD payloadSize = sizeof(payload);

    FILE *stream = fopen("encrypted.txt", "rb");
    if (!stream)
        return 1;

    fread(payload, 1, sizeof(payload), stream);
    fclose(stream);

    printf("key: ");
    if (!fgets(secret, sizeof(secret), stdin))
        return 1;

    secret[strcspn(secret, "\n")] = 0;

    HCRYPTPROV provider = init_provider();
    if (!provider)
        return 1;

    HCRYPTHASH digest = build_digest(provider, secret);
    if (!digest)
        return 1;

    if (!unlock_payload(provider, digest, payload, &payloadSize))
        return 1;

    payload[payloadSize] = '\0';
    puts(payload);

    CryptDestroyHash(digest);
    CryptReleaseContext(provider, 0);

    return 0;
}