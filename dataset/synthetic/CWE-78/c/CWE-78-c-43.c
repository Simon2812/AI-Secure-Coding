#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

static int verbose_mode = 0;

int main(int ac, char **av)
{
    int rc = 0;
    char tmp[400];
    char *mode = NULL;

    if (ac < 2) {
        printf("need argument\n");
        return 1;
    }

    mode = getenv("APP_MODE");
    if (mode && strcmp(mode, "debug") == 0)
        verbose_mode = 1;

    strcpy(tmp, "date ");
    strcat(tmp, av[1]);

    if (verbose_mode)
        printf("running: %s\n", tmp);

    rc = system(tmp);

    if (rc != 0)
        goto fail;

    return 0;

fail:
    printf("error\n");
    return 1;
}