#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    FILE *f = fopen("job.cfg", "r");
    if (!f)
        return 1;

    char line[256];
    if (!fgets(line, sizeof(line), f)) {
        fclose(f);
        return 1;
    }
    fclose(f);

    size_t n = strlen(line);
    if (n > 0 && line[n - 1] == '\n')
        line[n - 1] = '\0';

    for (char *p = line; *p; ++p) {
        if (*p == ';')
            *p = '\0';
    }

    char cmd[300];
    snprintf(cmd, sizeof(cmd), "ping -c 1 %s", line);

    return system(cmd);
}