#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    if (argc != 2)
        return 1;

    char cmd[512];
    snprintf(cmd, sizeof(cmd),
             "ps aux | grep %s | wc -l",
             argv[1]);

    FILE *fp = popen(cmd, "r");
    if (!fp)
        return 1;

    char buf[64];
    if (fgets(buf, sizeof(buf), fp))
        printf("matches: %s", buf);

    pclose(fp);
    return 0;
}