#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    int n = atoi(argv[1]);
    int size = n * sizeof(int);
    int *buf = malloc(size);
    if (!buf) return 1;
    for (int i = 0; i < n; i++) buf[i] = i;
    free(buf);
    return 0;
}
