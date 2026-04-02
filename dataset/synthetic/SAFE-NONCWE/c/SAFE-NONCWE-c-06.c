#include <stdio.h>

typedef struct {
    int id;
    int category;
    double price;
    int quantity;
} Item;

double compute_item_value(const Item *item) {
    return item->price * item->quantity;
}

double compute_category_total(const Item *items, int count, int category) {
    double total = 0.0;
    int i;

    for (i = 0; i < count; ++i) {
        if (items[i].category == category) {
            total += compute_item_value(&items[i]);
        }
    }

    return total;
}

int find_highest_value_item(const Item *items, int count) {
    int i;
    int index = -1;
    double best = 0.0;

    for (i = 0; i < count; ++i) {
        double value = compute_item_value(&items[i]);
        if (index == -1 || value > best) {
            best = value;
            index = i;
        }
    }

    return index;
}

int main(void) {
    Item items[] = {
        {1, 1, 12.5, 10},
        {2, 2, 5.0, 50},
        {3, 1, 20.0, 3},
        {4, 3, 7.5, 25},
        {5, 2, 2.0, 100}
    };

    int count = sizeof(items) / sizeof(items[0]);

    double total_inventory = 0.0;
    int i;

    for (i = 0; i < count; ++i) {
        total_inventory += compute_item_value(&items[i]);
    }

    double cat1 = compute_category_total(items, count, 1);
    double cat2 = compute_category_total(items, count, 2);
    double cat3 = compute_category_total(items, count, 3);

    int best_index = find_highest_value_item(items, count);

    printf("Total inventory value: %.2f\n", total_inventory);
    printf("Category 1 value: %.2f\n", cat1);
    printf("Category 2 value: %.2f\n", cat2);
    printf("Category 3 value: %.2f\n", cat3);

    if (best_index >= 0) {
        printf("Top item ID: %d\n", items[best_index].id);
    }

    return 0;
}