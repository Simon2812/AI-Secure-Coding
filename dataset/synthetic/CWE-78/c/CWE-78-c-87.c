#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_headers(char *mode, size_t mc, char *x, size_t xc) {
    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        if (line[0] == '\n' || line[0] == '\r') break;

        if (strncmp(line, "Mode: ", 6) == 0) {
            strncpy(mode, line + 6, mc - 1);
            mode[mc - 1] = '\0';
        } else if (strncmp(line, "X: ", 3) == 0) {
            strncpy(x, line + 3, xc - 1);
            x[xc - 1] = '\0';
        }
    }

    for (size_t i = 0; mode[i]; i++)
        if (mode[i] == '\n' || mode[i] == '\r') { mode[i] = '\0'; break; }
    for (size_t i = 0; x[i]; i++)
        if (x[i] == '\n' || x[i] == '\r') { x[i] = '\0'; break; }

    return mode[0] != '\0';
}

int main(void) {
    char mode[32] = "";
    char x[64] = "";
    if (!read_headers(mode, sizeof(mode), x, sizeof(x))) return 1;

    (void)x;

    if (strcmp(mode, "a") == 0) return system("echo A | tr A-Z a-z") == 0 ? 0 : 1;
    if (strcmp(mode, "b") == 0) return system("echo B | tr A-Z a-z") == 0 ? 0 : 1;
    return system("echo C | tr A-Z a-z") == 0 ? 0 : 1;
}