#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void render(char *dst, size_t cap, const char *tmpl, const char *x)
{
    const char *p = strstr(tmpl, "{x}");
    if (!p) { snprintf(dst, cap, "%s", tmpl); return; }

    size_t pre = (size_t)(p - tmpl);
    snprintf(dst, cap, "%.*s%s%s", (int)pre, tmpl, x, p + 3);
}

static int clean(const char *s)
{
    for (const unsigned char *p = (const unsigned char *)s; *p; ++p)
        if (*p == '\'' || *p == '"' || *p == '`' || *p == '$')
            return 0;
    return 1;
}

int main(int argc, char **argv)
{
    const char *x = (argc >= 2) ? argv[1] : "info";
    if (!clean(x)) return 1;

    char cmd[256];
    render(cmd, sizeof(cmd), "echo '{x}' | tr a-z A-Z", x);

    FILE *p = popen(cmd, "r");
    if (!p) return 1;

    char out[128];
    while (fgets(out, sizeof(out), p))
        fputs(out, stdout);

    pclose(p);
    return 0;
}