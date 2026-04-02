#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int load_profile(char *out, size_t cap) {
    FILE *f = fopen("profile.ini", "r");
    if (!f) return 0;
    if (!fgets(out, cap, f)) { fclose(f); return 0; }
    fclose(f);
    size_t n = strlen(out);
    while (n && (out[n-1] == '\n' || out[n-1] == '\r')) out[--n] = '\0';
    return n > 0;
}

static int pick(const char *s) {
    if (!s) return 0;
    if (strcmp(s, "a") == 0) return 1;
    if (strcmp(s, "b") == 0) return 2;
    if (strcmp(s, "c") == 0) return 3;
    return 0;
}

int main(int argc, char **argv) {
    char prof[64] = {0};
    const char *sel = (argc >= 2) ? argv[1] : NULL;

    if (!sel) {
        if (load_profile(prof, sizeof(prof)))
            sel = prof;
    }

    int m = pick(sel);
    if (m == 0) m = 2;

    if (m == 1) return system("df -h") == 0 ? 0 : 1;
    if (m == 2) return system("uname -a") == 0 ? 0 : 1;
    return system("whoami") == 0 ? 0 : 1;
}