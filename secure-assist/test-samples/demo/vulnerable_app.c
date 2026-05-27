#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Process user-supplied packet */
void process_packet(int data_len, const char *payload) {
    /* CWE-190: integer overflow in size calculation */
    int buf_size = data_len + 16;
    char *buf = malloc(buf_size);
    if (!buf) return;

    /* CWE-787: strcpy with no bounds check */
    strcpy(buf, payload);
    printf("Packet: %s\n", buf);
    free(buf);

    /* CWE-416: use after free */
    printf("Length: %zu\n", strlen(buf));
}

int main(int argc, char *argv[]) {
    if (argc < 3) return 1;
    int len = atoi(argv[1]);
    process_packet(len, argv[2]);
    return 0;
}
