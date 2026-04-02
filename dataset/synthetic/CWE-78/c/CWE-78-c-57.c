#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int starts_with(const char *s, const char *pfx)
{
    return strncmp(s, pfx, strlen(pfx)) == 0;
}

int main(void)
{
    char line[256];
    char agent[128] = "";
    char query[128] = "";

    while (fgets(line, sizeof(line), stdin)) {
        size_t n = strlen(line);
        if (n > 0 && line[n - 1] == '\n')
            line[n - 1] = '\0';

        if (line[0] == '\0')
            break;

        if (starts_with(line, "Agent: ")) {
            strncpy(agent, line + 7, sizeof(agent) - 1);
        } else if (starts_with(line, "Query: ")) {
            strncpy(query, line + 7, sizeof(query) - 1);
        }
    }

    if (agent[0] == '\0' || query[0] == '\0')
        return 1;

    char cmd[512];
    snprintf(cmd, sizeof(cmd), "%s %s", agent, query);

    FILE *fp = popen(cmd, "r");
    if (!fp)
        return 1;

    char out[256];
    while (fgets(out, sizeof(out), fp))
        fputs(out, stdout);

    pclose(fp);
    return 0;
}