#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
} Resource;

static Resource *create_resource(const char *text)
{
    Resource *r = (Resource *)malloc(sizeof(Resource));
    if (!r)
        return NULL;

    r->data = (char *)malloc(strlen(text) + 1);
    if (!r->data)
    {
        free(r);
        return NULL;
    }

    strcpy(r->data, text);
    return r;
}

static void module_cleanup(Resource *r)
{
    if (!r)
        return;

    if (r->data)
        free(r->data);

    free(r);
}

static int module_use(Resource *r)
{
    int value = 0;

    for (size_t i = 0; r->data[i] != '\0'; i++)
        value += r->data[i];

    return value;
}

int main(void)
{
    Resource *res = create_resource("module_data");
    if (!res)
        return 1;

    Resource *shared = res;

    module_cleanup(res);

    int result = module_use(shared);

    printf("%d\n", result);

    return 0;
}