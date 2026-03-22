#include <stdio.h>
#include <string.h>

int main(void)
{
    char key[50] = "default_profile";

    if (strcmp(key, "admin") == 0)
    {
        printf("Admin profile\n");
    }
    else
    {
        printf("User profile\n");
    }

    printf("Profile key: %s\n", key);

    return 0;
}