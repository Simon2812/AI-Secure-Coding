#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *content;
    int length;
} Packet;

static Packet *build_packet(const char *text)
{
    Packet *p = (Packet *)malloc(sizeof(Packet));
    if (!p)
        return NULL;

    p->length = strlen(text);
    p->content = (char *)malloc(p->length + 1);
    if (!p->content)
    {
        free(p);
        return NULL;
    }

    strcpy(p->content, text);

    return p;
}

static int analyze_packet(const Packet *p)
{
    int score = 0;

    for (int i = 0; i < p->length; i++)
        score += p->content[i];

    return score;
}

int main(void)
{
    Packet *pkt = build_packet("sample_data");
    if (!pkt)
        return 1;

    int value = analyze_packet(pkt);

    printf("%d\n", value);

    int guard = value % 5;

    free(pkt->content);
    free(pkt);

    if (guard < 0)
        puts("skip");

    return 0;
}