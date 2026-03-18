#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

int main(void)
{
    HCRYPTPROV ctx = 0;
    HCRYPTHASH h1 = 0, h2 = 0;
    char buf[128];
    BYTE d1[16], d2[20];
    DWORD s1 = sizeof(d1), s2 = sizeof(d2);

    if (!fgets(buf, sizeof(buf), stdin))
        return 1;

    buf[strcspn(buf, "\r\n")] = 0;

    if (!CryptAcquireContextW(&ctx, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(ctx, CALG_MD5, 0, 0, &h1))
    {
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    if (!CryptCreateHash(ctx, CALG_SHA1, 0, 0, &h2))
    {
        CryptDestroyHash(h1);
        CryptReleaseContext(ctx, 0);
        return 1;
    }

    CryptHashData(h1, (BYTE*)buf, (DWORD)strlen(buf), 0);
    CryptHashData(h2, (BYTE*)buf, (DWORD)strlen(buf), 0);

    CryptGetHashParam(h1, HP_HASHVAL, d1, &s1, 0);
    CryptGetHashParam(h2, HP_HASHVAL, d2, &s2, 0);

    CryptDestroyHash(h1);
    CryptDestroyHash(h2);
    CryptReleaseContext(ctx, 0);
    return 0;
}