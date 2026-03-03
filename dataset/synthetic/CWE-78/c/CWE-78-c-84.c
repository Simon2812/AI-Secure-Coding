#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_kv(const char *path, char *k, size_t kc, char *v, size_t vc) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;

    char line[256];
    while (fgets(line, sizeof(line), f)) {
        char *eq = strchr(line, '=');
        if (!eq) continue;
        *eq = '\0';
        char *val = eq + 1;

        size_t n = strlen(val);
        while (n && (val[n-1] == '\n' || val[n-1] == '\r')) val[--n] = '\0';

        if (strcmp(line, "mode") == 0) {
            strncpy(v, val, vc - 1); v[vc - 1] = '\0';
            strncpy(k, line, kc - 1); k[kc - 1] = '\0';
            fclose(f);
            return 1;
        }
    }

    fclose(f);
    return 0;
}

int main(void) {
    char k[16], mode[32] = "time";
    (void)read_kv("settings.cfg", k, sizeof(k), mode, sizeof(mode));

    FILE *p = NULL;

    if (strcmp(mode, "time") == 0) {
        p = popen("date -u | sed -n '1p'", "r");
    } else if (strcmp(mode, "user") == 0) {
        p = popen("id | sed -n '1p'", "r");
    } else {
        p = popen("uname -a | sed -n '1p'", "r");
    }

    if (!p) return 1;

    char out[256];
    while (fgets(out, sizeof(out), p)) fputs(out, stdout);
    pclose(p);
    return 0;
}