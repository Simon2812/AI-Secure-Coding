#include <stdio.h>
#include <string.h>

int main(void)
{
    char password[50] = "ABCD1234!";

    if (strlen(password) > 5)
    {
        printf("Length OK\n");
    }

    if (strcmp(password, "ABCD1234!") == 0)
    {
        printf("Match\n");
    }

    printf("Value: %s\n", password);

    return 0;
}