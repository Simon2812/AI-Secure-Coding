#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char header[32];
    char payload[64];
} Message;

static void init_message(Message *msg)
{
    strncpy(msg->header, "info", sizeof(msg->header) - 1);
    msg->header[sizeof(msg->header) - 1] = '\0';

    strncpy(msg->payload, "empty", sizeof(msg->payload) - 1);
    msg->payload[sizeof(msg->payload) - 1] = '\0';
}

static void load_message(Message *msg, int argc, char *argv[])
{
    if (argc > 1)
    {
        sprintf(msg->header, "%s", argv[1]);
    }

    if (argc > 2)
    {
        memcpy(msg->payload, argv[2], strlen(argv[2]));
        msg->payload[sizeof(msg->payload) - 1] = '\0';
    }
}

static void print_message(const Message *msg)
{
    printf("Header: %s\n", msg->header);
    printf("Payload: %s\n", msg->payload);
}

static void format_output(const Message *msg)
{
    char buffer[128];

    snprintf(buffer, sizeof(buffer), "[%s] %s", msg->header, msg->payload);
    printf("%s\n", buffer);
}

int main(int argc, char *argv[])
{
    Message msg;

    init_message(&msg);
    load_message(&msg, argc, argv);

    print_message(&msg);
    format_output(&msg);

    return 0;
}