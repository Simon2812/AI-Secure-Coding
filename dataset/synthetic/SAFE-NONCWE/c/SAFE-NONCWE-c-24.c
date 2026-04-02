#include <stdio.h>
#include <string.h>

#define MAX_ITEMS 64
#define NAME_LEN 32

typedef struct {
    char name[NAME_LEN];
    double price;
} CatalogItem;

typedef struct {
    char name[NAME_LEN];
    int quantity;
} OrderLine;

typedef struct {
    OrderLine lines[MAX_ITEMS];
    int line_count;
} Order;

typedef struct {
    double subtotal;
    double tax;
    double total;
} Invoice;

int find_catalog_item(const CatalogItem catalog[], int count, const char *name) {
    int i;
    for (i = 0; i < count; ++i) {
        if (strcmp(catalog[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

int validate_order(const Order *order) {
    int i;

    if (order->line_count <= 0) {
        return 0;
    }

    for (i = 0; i < order->line_count; ++i) {
        if (order->lines[i].quantity <= 0) {
            return 0;
        }

        if (order->lines[i].name[0] == '\0') {
            return 0;
        }
    }

    return 1;
}

double compute_subtotal(const Order *order, const CatalogItem catalog[], int catalog_size) {
    int i;
    double total = 0.0;

    for (i = 0; i < order->line_count; ++i) {
        int idx = find_catalog_item(catalog, catalog_size, order->lines[i].name);

        if (idx >= 0) {
            total += catalog[idx].price * order->lines[i].quantity;
        } else {
            printf("Warning: item '%s' not found in catalog\n", order->lines[i].name);
        }
    }

    return total;
}

double compute_tax(double subtotal, double rate) {
    return subtotal * rate;
}

void build_invoice(const Order *order,
                   const CatalogItem catalog[],
                   int catalog_size,
                   Invoice *invoice) {

    double subtotal = compute_subtotal(order, catalog, catalog_size);
    double tax = compute_tax(subtotal, 0.17);

    invoice->subtotal = subtotal;
    invoice->tax = tax;
    invoice->total = subtotal + tax;
}

void print_invoice(const Order *order,
                   const CatalogItem catalog[],
                   int catalog_size,
                   const Invoice *invoice) {

    int i;

    printf("Invoice\n");
    printf("-------\n");

    for (i = 0; i < order->line_count; ++i) {
        int idx = find_catalog_item(catalog, catalog_size, order->lines[i].name);

        if (idx >= 0) {
            double line_total = catalog[idx].price * order->lines[i].quantity;

            printf("%s x%d -> %.2f\n",
                   order->lines[i].name,
                   order->lines[i].quantity,
                   line_total);
        }
    }

    printf("\nSubtotal: %.2f\n", invoice->subtotal);
    printf("Tax: %.2f\n", invoice->tax);
    printf("Total: %.2f\n", invoice->total);
}

int main(void) {
    CatalogItem catalog[] = {
        {"coffee", 3.5},
        {"sandwich", 7.0},
        {"juice", 4.0},
        {"cake", 5.5}
    };

    int catalog_size = sizeof(catalog) / sizeof(catalog[0]);

    Order order;
    order.line_count = 3;

    snprintf(order.lines[0].name, NAME_LEN, "%s", "coffee");
    order.lines[0].quantity = 2;

    snprintf(order.lines[1].name, NAME_LEN, "%s", "cake");
    order.lines[1].quantity = 1;

    snprintf(order.lines[2].name, NAME_LEN, "%s", "juice");
    order.lines[2].quantity = 3;

    if (!validate_order(&order)) {
        printf("Invalid order\n");
        return 1;
    }

    Invoice invoice;
    build_invoice(&order, catalog, catalog_size, &invoice);

    print_invoice(&order, catalog, catalog_size, &invoice);

    return 0;
}