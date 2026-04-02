#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void build(char *dst, size_t cap, const char *a, const char *b)
{
    char tmp[128];
    snprintf(tmp, sizeof(tmp), "%s:%s", a, b);
    snprintf(dst, cap, "%s", tmp);
}

int main(int argc, char **argv)
{
    const char *left = "tag";
    const char *right = (argc >= 2) ? argv[1] : "none";

    char payload[256];
    build(payload, sizeof(payload), left, right);

    char *args[] = {"logger", payload, NULL};
    execvp("logger", args);
    return 1;
}