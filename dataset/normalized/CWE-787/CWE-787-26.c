#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 27015
#define HOST "127.0.0.1"
#define BUF_SIZE 32

void allocate_from_socket()
{
    int value = -1;

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return;

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = inet_addr(HOST);

    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) == 0)
    {
        char buf[BUF_SIZE];
        int received = recv(sock, buf, BUF_SIZE - 1, 0);
        if (received > 0)
        {
            buf[received] = '\0';
            value = atoi(buf);
        }
    }

    close(sock);

    int *ptr = malloc(value * sizeof(int));
    if (!ptr) exit(1);

    for (size_t i = 0; i < (size_t)value; i++)
    {
        ptr[i] = 0;
    }

    printf("%d\n", ptr[0]);
    free(ptr);
}

int main()
{
    allocate_from_socket();
    return 0;
}