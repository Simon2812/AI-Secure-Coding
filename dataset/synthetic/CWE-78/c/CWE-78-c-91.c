#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void to_lower(char *s) {
    for (size_t i = 0; s[i]; i++)
        if (s[i] >= 'A' && s[i] <= 'Z') s[i] = (char)(s[i] - 'A' + 'a');
}

int main(int argc, char **argv) {
    char label[48] = "default";
    if (argc >= 2) {
        strncpy(label, argv[1], sizeof(label) - 1);
        label[sizeof(label) - 1] = '\0';
    }
    to_lower(label);

    if (strcmp(label, "a") != 0 && strcmp(label, "b") != 0 && strcmp(label, "c") != 0)
        strcpy(label, "default");

    char msg[96];
    snprintf(msg, sizeof(msg), "state=%s", label);

    char *a[] = { "printf", "%s\n", msg, NULL };
    execvp("printf", a);
    return 1;
}