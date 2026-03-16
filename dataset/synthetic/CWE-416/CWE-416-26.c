#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *payload;
    int length;
} Frame;

static Frame *create_frame(const char *msg)
{
    Frame *f = (Frame *)malloc(sizeof(Frame));
    if (!f)
        return NULL;

    f->length = strlen(msg);
    f->payload = (char *)malloc(f->length + 1);
    if (!f->payload)
    {
        free(f);
        return NULL;
    }

    strcpy(f->payload, msg);
    return f;
}

static void release_frame(Frame *f)
{
    if (!f)
        return;

    if (f->payload)
        free(f->payload);

    free(f);
}

static int accumulate(const char *data)
{
    int sum = 0;

    for (size_t i = 0; data[i] != '\0'; i++)
        sum += data[i];

    return sum;
}

int main(void)
{
    Frame *frame = create_frame("network_packet");
    if (!frame)
        return 1;

    const char *view = frame->payload;

    release_frame(frame);

    int result = accumulate(view);

    printf("%d\n", result);

    return 0;
}