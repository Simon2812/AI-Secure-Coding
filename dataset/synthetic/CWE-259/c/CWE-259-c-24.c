#include <stdio.h>
#include <string.h>

int main(void)
{
    char raw[] = "ABCD1234!";
    char encoded[50];
    int i;

    for (i = 0; i < (int)strlen(raw); i++)
    {
        encoded[i] = raw[i] ^ 0x2A;
    }
    encoded[i] = '\0';

    printf("Encoded value: ");
    for (i = 0; i < (int)strlen(raw); i++)
    {
        printf("%02X", (unsigned char)encoded[i]);
    }
    printf("\n");

    return 0;
}