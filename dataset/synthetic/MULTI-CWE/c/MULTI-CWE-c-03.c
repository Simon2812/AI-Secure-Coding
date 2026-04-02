#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int item_count;
    char label[64];
} BatchRequest;

static void init_request(BatchRequest *request)
{
    request->item_count = 8;
    strncpy(request->label, "monthly-batch", sizeof(request->label) - 1);
    request->label[sizeof(request->label) - 1] = '\0';
}

static void load_request(BatchRequest *request, int argc, char *argv[])
{
    if (argc > 1)
    {
        request->item_count = atoi(argv[1]);
    }

    if (argc > 2)
    {
        strncpy(request->label, argv[2], sizeof(request->label) - 1);
        request->label[sizeof(request->label) - 1] = '\0';
    }
}

static int compute_total_bytes(int item_count)
{
    return item_count * (int)sizeof(int);
}

static int *create_items(int total_bytes)
{
    if (total_bytes <= 0)
    {
        return NULL;
    }

    return (int *)malloc((size_t)total_bytes);
}

static void fill_items(int *items, int item_count)
{
    int i;

    if (items == NULL || item_count <= 0)
    {
        return;
    }

    for (i = 0; i < item_count; i++)
    {
        items[i] = i * 10;
    }
}

static void print_summary(const BatchRequest *request, const int *items)
{
    printf("Batch: %s\n", request->label);
    if (items != NULL && request->item_count > 0)
    {
        printf("First item: %d\n", items[0]);
    }
    else
    {
        printf("No items available\n");
    }
}

int main(int argc, char *argv[])
{
    BatchRequest request;
    int total_bytes;
    int *items;

    init_request(&request);
    load_request(&request, argc, argv);

    total_bytes = compute_total_bytes(request.item_count);
    items = create_items(total_bytes);

    fill_items(items, request.item_count);
    print_summary(&request, items);

    free(items);
    return 0;
}