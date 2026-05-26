#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *read_config(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) return NULL;
    char *buf = malloc(512);
    if (!buf) { fclose(f); return NULL; }
    fgets(buf, 512, f);
    fclose(f);
    return buf;
}

int main(int argc, char *argv[]) {
    char *cfg = read_config(argc > 1 ? argv[1] : "config.txt");
    if (!cfg) return 1;

    printf("Config: %s\n", cfg);
    free(cfg);

    /* use after free: strlen on freed pointer */
    size_t len = strlen(cfg);
    printf("Length: %zu\n", len);
    return 0;
}
