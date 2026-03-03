#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static int ok_service_name(const char *s)
{
    if (!s || s[0] == '\0')
        return 0;
    if (s[0] == '-')
        return 0;

    for (const unsigned char *p = (const unsigned char *)s; *p; ++p) {
        if (!(isalnum(*p) || *p == '@' || *p == '.' || *p == '_' || *p == '-'))
            return 0;
    }
    return 1;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s <service>\n", argv[0]);
        return 1;
    }

    const char *svc = argv[1];

    char cmd[512];
    snprintf(cmd, sizeof(cmd),
             "systemctl restart %s && systemctl --no-pager --full status %s",
             svc, svc);

    int rc = system(cmd);
    return (rc == 0) ? 0 : 1;
}