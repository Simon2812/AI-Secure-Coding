#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void build_label(char *dst, size_t cap, const char *prefix, const char *name) {
    snprintf(dst, cap, "%s:%s", prefix, name ? name : "none");
}

static int is_small(const char *s) {
    return s && strlen(s) <= 40;
}

int main(int argc, char **argv) {
    const char *tag = (argc >= 2) ? argv[1] : getenv("TAG");
    if (!is_small(tag)) tag = "default";

    char msg[128];
    build_label(msg, sizeof(msg), "job", tag);

    char *a[] = { "logger", msg, NULL };
    execvp("logger", a);
    return 1;
}