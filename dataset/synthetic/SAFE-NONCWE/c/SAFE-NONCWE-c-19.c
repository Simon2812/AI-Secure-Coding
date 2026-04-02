#include <stdio.h>
#include <string.h>

typedef struct {
    int id;
    int days_present;
    int days_late;
} Employee;

int parse_line(const char *line, Employee *e) {
    int id, present, late;

    if (sscanf(line, "%d %d %d", &id, &present, &late) != 3) {
        return 0;
    }

    if (id <= 0 || present < 0 || late < 0) {
        return 0;
    }

    e->id = id;
    e->days_present = present;
    e->days_late = late;
    return 1;
}

int load_employees(const char *path, Employee list[], int max) {
    FILE *fp = fopen(path, "r");
    char line[256];
    int count = 0;

    if (!fp) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp)) {
        Employee e;

        if (count >= max) {
            break;
        }

        if (parse_line(line, &e)) {
            list[count++] = e;
        }
    }

    fclose(fp);
    return count;
}

double compute_attendance_rate(const Employee *e) {
    int total_days = e->days_present + e->days_late;

    if (total_days == 0) {
        return 0.0;
    }

    return (double)e->days_present / total_days;
}

double average_attendance(const Employee list[], int count) {
    int i;
    double total = 0.0;

    for (i = 0; i < count; ++i) {
        total += compute_attendance_rate(&list[i]);
    }

    if (count == 0) {
        return 0.0;
    }

    return total / count;
}

int find_most_reliable(const Employee list[], int count) {
    int i;
    int best = -1;
    double best_score = -1.0;

    for (i = 0; i < count; ++i) {
        double rate = compute_attendance_rate(&list[i]);

        if (best == -1 || rate > best_score) {
            best = i;
            best_score = rate;
        }
    }

    return best;
}

void print_summary(const Employee list[], int count) {
    int i;

    printf("Employee Attendance Summary\n");
    printf("---------------------------\n");

    for (i = 0; i < count; ++i) {
        double rate = compute_attendance_rate(&list[i]);

        printf("ID: %d | Present: %d | Late: %d | Rate: %.2f\n",
               list[i].id,
               list[i].days_present,
               list[i].days_late,
               rate);
    }

    printf("\nAverage attendance rate: %.2f\n", average_attendance(list, count));

    int idx = find_most_reliable(list, count);
    if (idx >= 0) {
        printf("Most reliable employee ID: %d\n", list[idx].id);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <attendance_file>\n", argv[0]);
        return 1;
    }

    Employee employees[100];
    int count = load_employees(argv[1], employees, 100);

    if (count == 0) {
        printf("No valid data found.\n");
        return 1;
    }

    print_summary(employees, count);
    return 0;
}