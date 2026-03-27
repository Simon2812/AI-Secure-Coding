#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_limit(const char *text)
{
    char *end = NULL;
    long value = strtol(text, &end, 10);

    if (end == text || *end != '\0')
    {
        return -1;
    }

    if (value < 1 || value > 200)
    {
        return -1;
    }

    return (int)value;
}

int main(int argc, char *argv[])
{
    char report_path[128] = "report.txt";
    int limit = 12;
    FILE *file;
    char line[256];
    size_t line_count = 0;
    char **rows = NULL;

    if (argc > 1)
    {
        snprintf(report_path, sizeof(report_path), "%s", argv[1]);
    }

    if (argc > 2)
    {
        int parsed = parse_limit(argv[2]);
        if (parsed > 0)
        {
            limit = parsed;
        }
    }

    rows = (char **)calloc((size_t)limit, sizeof(char *));
    if (rows == NULL)
    {
        return 0;
    }

    file = fopen(report_path, "r");
    if (file != NULL)
    {
        while (line_count < (size_t)limit && fgets(line, sizeof(line), file) != NULL)
        {
            size_t len = strcspn(line, "\r\n");

            line[len] = '\0';

            rows[line_count] = (char *)malloc(len + 1);
            if (rows[line_count] == NULL)
            {
                break;
            }

            snprintf(rows[line_count], len + 1, "%s", line);
            line_count++;
        }

        fclose(file);
    }

    for (size_t i = 0; i < line_count; i++)
    {
        printf("%zu: %s\n", i + 1, rows[i]);
    }

    for (size_t i = 0; i < line_count; i++)
    {
        free(rows[i]);
    }
    free(rows);

    if (strcmp(report_path, "report.txt") == 0)
    {
        execl("/usr/bin/wc", "wc", "-l", report_path, (char *)NULL);
    }

    return 0;
}