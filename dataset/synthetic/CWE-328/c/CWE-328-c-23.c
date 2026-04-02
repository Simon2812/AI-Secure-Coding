#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "advapi32.lib")

#define LIMIT 128
#define LEN (256 / 8)

int main(void)
{
    FILE *f = fopen("password.txt", "r");
    UCHAR ref[LEN], cur[LEN];
    char data[LIMIT];
    size_t i;
    DWORD size = LEN;
    HCRYPTPROV p = 0;
    HCRYPTHASH h = 0;
    int match = 1;

    if (!f) return 1;

    for (i = 0; i < LEN; i++)
    {
        ULONG v;
        if (fscanf(f, "%02x", &v) != 1 || v > 0xff)
        {
            fclose(f);
            return 1;
        }
        ref[i] = (UCHAR)v;
    }
    fclose(f);

    if (!fgets(data, sizeof(data), stdin))
        return 1;

    data[strcspn(data, "\n")] = 0;

    if (!CryptAcquireContextW(&p, NULL, NULL, PROV_RSA_FULL, 0))
        return 1;

    if (!CryptCreateHash(p, CALG_SHA_256, 0, 0, &h))
    {
        CryptReleaseContext(p, 0);
        return 1;
    }

    CryptHashData(h, (BYTE*)data, (DWORD)strlen(data), 0);
    CryptGetHashParam(h, HP_HASHVAL, cur, &size, 0);

    for (i = 0; i < LEN; i++)
    {
        if (ref[i] != cur[i])
        {
            match = 0;
            break;
        }
    }

    puts(match ? "OK" : "FAIL");

    CryptDestroyHash(h);
    CryptReleaseContext(p, 0);
    return 0;
}