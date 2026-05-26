#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *global_buf = NULL;

void init(void) {
    global_buf = malloc(256);
    if (global_buf) strcpy(global_buf, "initialized");
}

void cleanup(void) {
    free(global_buf);
}

void report(void) {
    /* use after free: cleanup() may have already freed global_buf */
    printf("buf: %s\n", global_buf);
}

int main(void) {
    init();
    cleanup();
    report();
    return 0;
}
