#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int split2(char *s, char **a, char **b) {
    char *p = strchr(s, ':');
    if (!p) return 0;
    *p = '\0';
    *a = s;
    *b = p + 1;
    return 1;
}

int main(void) {
    char line[256];
    if (!fgets(line, sizeof(line), stdin)) return 1;

    size_t n = strlen(line);
    while (n && (line[n-1] == '\n' || line[n-1] == '\r')) line[--n] = '\0';

    char *k = NULL, *v = NULL;
    if (!split2(line, &k, &v)) return 1;

    char cmd[256];

    if (strcmp(k, "mode") == 0 && strcmp(v, "mini") == 0) {
        snprintf(cmd, sizeof(cmd), "ps -eo comm | head -n 3");
    } else if (strcmp(k, "mode") == 0 && strcmp(v, "full") == 0) {
        snprintf(cmd, sizeof(cmd), "ps -eo comm | head -n 10");
    } else {
        snprintf(cmd, sizeof(cmd), "ps -eo comm | head -n 1");
    }

    FILE *p = popen(cmd, "r");
    if (!p) return 1;
    char out[256];
    while (fgets(out, sizeof(out), p)) fputs(out, stdout);
    pclose(p);
    return 0;
}