#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void write_block(unsigned char *dst, int offset, const unsigned char *src, int length)
{
    memcpy(dst + offset, src, length);
}

static void assemble_packet(void)
{
    unsigned char packet[32];
    unsigned char block[16];
    char line[32];
    int offset;
    int i;

    memset(packet, 0, sizeof(packet));

    for (i = 0; i < 16; i++)
    {
        block[i] = (unsigned char)(i + 1);
    }

    if (fgets(line, sizeof(line), stdin) == NULL)
    {
        return;
    }

    offset = atoi(line);

    write_block(packet, offset, block, 16);

    for (i = 0; i < 32; i++)
    {
        printf("%u\n", packet[i]);
    }
}

int main(void)
{
    printf("packet offset:\n");
    assemble_packet();
    return 0;
}