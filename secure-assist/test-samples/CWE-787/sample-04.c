#include <stdio.h>
#include <string.h>

struct Packet {
    char header[4];
    char payload[64];
};

void build_packet(struct Packet *pkt, const char *data) {
    strcpy(pkt->header, "PKT");
    strcat(pkt->payload, data);
}

int main(int argc, char *argv[]) {
    struct Packet p = {0};
    if (argc < 2) return 1;
    build_packet(&p, argv[1]);
    printf("header=%s payload=%s\n", p.header, p.payload);
    return 0;
}
