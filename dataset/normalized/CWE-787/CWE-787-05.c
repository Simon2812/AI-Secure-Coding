#include <stdio.h>
#include <string.h>

void copy_text()
{
    char *ptr;
    char storage[15];

    ptr = storage;
    ptr[0] = '\0';

    char text[16] = "ABCDEABCDEABCDE";

    strcpy(ptr, text);

    printf("%s\n", ptr);
}

int main()
{
    copy_text();
    return 0;
}