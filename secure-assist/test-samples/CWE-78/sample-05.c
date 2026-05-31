#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void run_check(const char *host) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "nmap -sV %s", host);
    system(cmd);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    run_check(argv[1]);
    return 0;
}
