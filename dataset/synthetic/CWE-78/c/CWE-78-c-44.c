#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    FILE *f = fopen("input.txt", "r");
    if (!f) {
        printf("missing input.txt\n");
        return 1;
    }

    char key[128];
    if (!fgets(key, sizeof(key), f)) {
        fclose(f);
        return 1;
    }
    fclose(f);

    size_t n = strlen(key);
    if (n > 0 && key[n - 1] == '\n')
        key[n - 1] = '\0';

    char cmd[256] = "echo ";
    strcat(cmd, key);

    FILE *p = popen(cmd, "r");
    if (!p)
        return 1;

    char out[256];
    while (fgets(out, sizeof(out), p))
        fputs(out, stdout);

    pclose(p);
    return 0;
}