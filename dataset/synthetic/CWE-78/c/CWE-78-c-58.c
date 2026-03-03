#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static int read_all(FILE *in, char *buf, size_t cap)
{
    size_t used = 0;
    while (used + 1 < cap) {
        size_t r = fread(buf + used, 1, cap - 1 - used, in);
        if (r == 0)
            break;
        used += r;
    }
    buf[used] = '\0';
    return (int)used;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s <subject>\n", argv[0]);
        return 1;
    }

    const char *to = getenv("NOTIFY_TO");
    if (!to || to[0] == '\0') {
        fprintf(stderr, "NOTIFY_TO not set\n");
        return 1;
    }

    char body[512];
    if (read_all(stdin, body, sizeof(body)) <= 0) {
        fprintf(stderr, "empty body\n");
        return 1;
    }

    char cmd[1024];
    snprintf(cmd, sizeof(cmd),
             "printf '%%s' \"%s\" | mail -s \"%s\" %s",
             body, argv[1], to);

    int rc = system(cmd);
    return (rc == 0) ? 0 : 1;
}