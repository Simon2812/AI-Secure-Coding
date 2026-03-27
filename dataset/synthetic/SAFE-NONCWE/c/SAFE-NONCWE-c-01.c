#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define LINE_CAP 256
#define NAME_CAP 64
#define MAX_RECORDS 128

typedef struct {
    char item[NAME_CAP];
    int quantity;
    double unit_price;
} SaleRecord;

static void trim_newline(char *text) {
    size_t len = strlen(text);
    if (len > 0 && text[len - 1] == '\n') {
        text[len - 1] = '\0';
    }
}

static void trim_spaces(char *text) {
    char *start = text;
    while (*start && isspace((unsigned char)*start)) {
        start++;
    }

    if (start != text) {
        memmove(text, start, strlen(start) + 1);
    }

    size_t len = strlen(text);
    while (len > 0 && isspace((unsigned char)text[len - 1])) {
        text[len - 1] = '\0';
        len--;
    }
}

static int parse_csv_line(const char *line, SaleRecord *record) {
    char item[NAME_CAP];
    int quantity = 0;
    double unit_price = 0.0;

    if (sscanf(line, " %63[^,] , %d , %lf", item, &quantity, &unit_price) != 3) {
        return 0;
    }

    trim_spaces(item);

    if (item[0] == '\0') {
        return 0;
    }

    if (quantity < 0 || unit_price < 0.0) {
        return 0;
    }

    snprintf(record->item, sizeof(record->item), "%s", item);
    record->quantity = quantity;
    record->unit_price = unit_price;
    return 1;
}

static int load_sales(const char *path, SaleRecord records[], size_t capacity, size_t *count) {
    FILE *fp = fopen(path, "r");
    char line[LINE_CAP];
    size_t used = 0;

    if (fp == NULL) {
        return 0;
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        SaleRecord record;

        trim_newline(line);

        if (line[0] == '\0') {
            continue;
        }

        if (used >= capacity) {
            break;
        }

        if (parse_csv_line(line, &record)) {
            records[used++] = record;
        }
    }

    fclose(fp);
    *count = used;
    return 1;
}

static double calculate_total_revenue(const SaleRecord records[], size_t count) {
    double total = 0.0;
    size_t i;

    for (i = 0; i < count; ++i) {
        total += records[i].quantity * records[i].unit_price;
    }

    return total;
}

static int find_top_item(const SaleRecord records[], size_t count) {
    size_t i;
    int best_index = -1;
    double best_value = -1.0;

    for (i = 0; i < count; ++i) {
        double current_value = records[i].quantity * records[i].unit_price;
        if (current_value > best_value) {
            best_value = current_value;
            best_index = (int)i;
        }
    }

    return best_index;
}

static void print_report(const SaleRecord records[], size_t count) {
    size_t i;
    double total_revenue = calculate_total_revenue(records, count);
    int top_index = find_top_item(records, count);

    printf("Sales report\n");
    printf("------------\n");
    printf("%-20s %-10s %-12s %-12s\n", "Item", "Quantity", "Unit Price", "Line Total");

    for (i = 0; i < count; ++i) {
        double line_total = records[i].quantity * records[i].unit_price;
        printf("%-20s %-10d %-12.2f %-12.2f\n",
               records[i].item,
               records[i].quantity,
               records[i].unit_price,
               line_total);
    }

    printf("\n");
    printf("Valid records: %zu\n", count);
    printf("Total revenue: %.2f\n", total_revenue);

    if (top_index >= 0) {
        double best_total = records[top_index].quantity * records[top_index].unit_price;
        printf("Top item: %s (%.2f)\n", records[top_index].item, best_total);
    }
}

int main(int argc, char *argv[]) {
    SaleRecord records[MAX_RECORDS];
    size_t count = 0;
    const char *path;

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <sales_file.csv>\n", argv[0]);
        return 1;
    }

    path = argv[1];

    if (!load_sales(path, records, MAX_RECORDS, &count)) {
        fprintf(stderr, "Could not open input file: %s\n", path);
        return 1;
    }

    print_report(records, count);
    return 0;
}