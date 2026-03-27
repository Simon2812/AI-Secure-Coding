#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define LINE_CAP 256
#define KEY_CAP 64
#define VALUE_CAP 128
#define MAX_ENTRIES 128

typedef struct {
    char key[KEY_CAP];
    char value[VALUE_CAP];
} ConfigEntry;

static void trim_newline(char *s) {
    size_t len = strlen(s);
    if (len > 0 && s[len - 1] == '\n') {
        s[len - 1] = '\0';
    }
}

static void trim_spaces(char *s) {
    char *start = s;
    while (*start && isspace((unsigned char)*start)) {
        start++;
    }

    if (start != s) {
        memmove(s, start, strlen(start) + 1);
    }

    size_t len = strlen(s);
    while (len > 0 && isspace((unsigned char)s[len - 1])) {
        s[len - 1] = '\0';
        len--;
    }
}

static int parse_line(const char *line, ConfigEntry *entry) {
    char buffer[LINE_CAP];
    char *eq;

    if (line[0] == '#' || line[0] == ';' || line[0] == '\0') {
        return 0;
    }

    snprintf(buffer, sizeof(buffer), "%s", line);

    eq = strchr(buffer, '=');
    if (!eq) {
        return 0;
    }

    *eq = '\0';
    char *key = buffer;
    char *value = eq + 1;

    trim_spaces(key);
    trim_spaces(value);

    if (key[0] == '\0') {
        return 0;
    }

    snprintf(entry->key, sizeof(entry->key), "%s", key);
    snprintf(entry->value, sizeof(entry->value), "%s", value);

    return 1;
}

static size_t load_config(const char *path, ConfigEntry entries[], size_t capacity) {
    FILE *fp = fopen(path, "r");
    char line[LINE_CAP];
    size_t count = 0;

    if (!fp) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        ConfigEntry e;

        trim_newline(line);

        if (count >= capacity) {
            break;
        }

        if (parse_line(line, &e)) {
            entries[count++] = e;
        }
    }

    fclose(fp);
    return count;
}

static const char *find_value(const ConfigEntry entries[], size_t count, const char *key) {
    size_t i;
    for (i = 0; i < count; ++i) {
        if (strcmp(entries[i].key, key) == 0) {
            return entries[i].value;
        }
    }
    return NULL;
}

static void print_all(const ConfigEntry entries[], size_t count) {
    size_t i;
    printf("Configuration entries:\n");
    printf("----------------------\n");
    for (i = 0; i < count; ++i) {
        printf("%s = %s\n", entries[i].key, entries[i].value);
    }
}

int main(int argc, char *argv[]) {
    ConfigEntry entries[MAX_ENTRIES];
    size_t count;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <config.ini>\n", argv[0]);
        return 1;
    }

    count = load_config(argv[1], entries, MAX_ENTRIES);

    if (count == 0) {
        fprintf(stderr, "No entries loaded or file not found.\n");
        return 1;
    }

    print_all(entries, count);

    const char *mode = find_value(entries, count, "mode");
    if (mode) {
        printf("\nMode is set to: %s\n", mode);
    }

    return 0;
}