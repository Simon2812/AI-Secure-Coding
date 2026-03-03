#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static void substitute(char *dst, size_t cap, const char *tmpl, const char *val)
{
    const char *p = strstr(tmpl, "%USER%");
    if (!p) {
        strncpy(dst, tmpl, cap - 1);
        dst[cap - 1] = '\0';
        return;
    }

    size_t prefix = p - tmpl;
    snprintf(dst, cap, "%.*s%s%s",
             (int)prefix,
             tmpl,
             val,
             p + 6);
}

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    const char *template = "id %USER%";
    char cmd[256];

    substitute(cmd, sizeof(cmd), template, argv[1]);

    FILE *fp = popen(cmd, "r");
    if (!fp)
        return 1;

    char buf[128];
    while (fgets(buf, sizeof(buf), fp))
        fputs(buf, stdout);

    pclose(fp);
    return 0;
}