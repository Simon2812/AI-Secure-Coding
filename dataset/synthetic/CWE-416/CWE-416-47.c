#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char key[16];
    char *value;
} Setting;

int main(void)
{
    Setting rows[3];
    int ok = 1;

    strcpy(rows[0].key, "mode");
    strcpy(rows[1].key, "theme");
    strcpy(rows[2].key, "lang");

    for (int i = 0; i < 3; i++)
    {
        rows[i].value = (char *)malloc(24);
        if (!rows[i].value)
        {
            ok = 0;
            break;
        }
    }

    if (!ok)
        return 1;

    strcpy(rows[0].value, "debug");
    strcpy(rows[1].value, "light");
    strcpy(rows[2].value, "en");

    FILE *fp = tmpfile();
    if (!fp)
        return 1;

    for (int i = 0; i < 3; i++)
    {
        fputs(rows[i].key, fp);
        fputc('=', fp);
        fputs(rows[i].value, fp);
        fputc('\n', fp);
    }

    rewind(fp);

    char line[64];
    int lines = 0;

    while (fgets(line, sizeof(line), fp) != NULL)
    {
        if (strchr(line, '=') != NULL)
            lines++;
    }

    fclose(fp);

    if (lines == 3)
        return 0;

    return 2;
}