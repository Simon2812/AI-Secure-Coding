#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int run_lookup(const char *name) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "nslookup %s", name);

    FILE *fp = popen(cmd, "r");
    if (!fp) {
        perror("popen");
        return 1;
    }

    char buf[256];
    while (fgets(buf, sizeof(buf), fp)) {
        fputs(buf, stdout);
    }

    int rc = pclose(fp);
    return (rc == 0) ? 0 : 1;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <host>\n", argv[0]);
        return 1;
    }

    const char *host = argv[1];
    if (host[0] == '\0') {
        fprintf(stderr, "Empty host\n");
        return 1;
    }

    return run_lookup(host);
}