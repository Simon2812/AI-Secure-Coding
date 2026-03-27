#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define LINE_CAP 256
#define NAME_CAP 64
#define MAX_STUDENTS 128
#define MAX_GRADES 10

typedef struct {
    char name[NAME_CAP];
    int grades[MAX_GRADES];
    size_t grade_count;
} Student;

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

static int parse_student_line(const char *line, Student *out) {
    char buffer[LINE_CAP];
    char *token;
    size_t count = 0;

    snprintf(buffer, sizeof(buffer), "%s", line);

    token = strtok(buffer, ",");
    if (token == NULL) {
        return 0;
    }

    trim_spaces(token);
    if (token[0] == '\0') {
        return 0;
    }

    snprintf(out->name, sizeof(out->name), "%s", token);
    out->grade_count = 0;

    while ((token = strtok(NULL, ",")) != NULL) {
        int grade;
        trim_spaces(token);

        if (out->grade_count >= MAX_GRADES) {
            break;
        }

        if (sscanf(token, "%d", &grade) != 1) {
            continue;
        }

        if (grade < 0 || grade > 100) {
            continue;
        }

        out->grades[out->grade_count++] = grade;
        count++;
    }

    return count > 0;
}

static int load_students(const char *path, Student students[], size_t capacity, size_t *count) {
    FILE *fp = fopen(path, "r");
    char line[LINE_CAP];
    size_t used = 0;

    if (!fp) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        Student s;

        trim_newline(line);

        if (line[0] == '\0') {
            continue;
        }

        if (used >= capacity) {
            break;
        }

        if (parse_student_line(line, &s)) {
            students[used++] = s;
        }
    }

    fclose(fp);
    *count = used;
    return 1;
}

static double compute_average(const Student *s) {
    size_t i;
    int sum = 0;

    if (s->grade_count == 0) {
        return 0.0;
    }

    for (i = 0; i < s->grade_count; ++i) {
        sum += s->grades[i];
    }

    return (double)sum / (double)s->grade_count;
}

static void print_report(const Student students[], size_t count) {
    size_t i;

    printf("Gradebook Report\n");
    printf("----------------\n");
    printf("%-20s %-10s %-10s\n", "Name", "Grades", "Average");

    for (i = 0; i < count; ++i) {
        const Student *s = &students[i];
        size_t j;

        printf("%-20s ", s->name);

        for (j = 0; j < s->grade_count; ++j) {
            printf("%d", s->grades[j]);
            if (j + 1 < s->grade_count) {
                printf(" ");
            }
        }

        if (s->grade_count == 0) {
            printf("N/A");
        }

        printf("   %-10.2f\n", compute_average(s));
    }
}

int main(int argc, char *argv[]) {
    Student students[MAX_STUDENTS];
    size_t count = 0;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <grades.csv>\n", argv[0]);
        return 1;
    }

    if (!load_students(argv[1], students, MAX_STUDENTS, &count)) {
        fprintf(stderr, "Failed to read file: %s\n", argv[1]);
        return 1;
    }

    print_report(students, count);
    return 0;
}