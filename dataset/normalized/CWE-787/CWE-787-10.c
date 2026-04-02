#include <stdio.h>
#include <string.h>

void transfer_string()
{
    char *text;
    char storage[30];

    text = storage;

    memset(text, 'A', 22);
    text[22] = '\0';

    char result[20] = "";

    strncpy(result, text, strlen(text));

    result[19] = '\0';

    printf("%s\n", text);
}

int main()
{
    transfer_string();
    return 0;
}