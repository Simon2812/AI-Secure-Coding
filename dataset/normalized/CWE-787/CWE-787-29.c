#include <iostream>
#include <cstdlib>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 27015
#define HOST "127.0.0.1"
#define INPUT_SIZE 32

void build_segment()
{
    int count = -1;

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return;

    sockaddr_in server;
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = inet_addr(HOST);

    if (connect(sock, (sockaddr*)&server, sizeof(server)) == 0)
    {
        char buf[INPUT_SIZE];
        int received = recv(sock, buf, INPUT_SIZE - 1, 0);
        if (received > 0)
        {
            buf[received] = '\0';
            count = atoi(buf);
        }
    }

    close(sock);

    size_t bytes = count * sizeof(int);
    int *segment = (int*)new char[bytes];

    for (size_t i = 0; i < (size_t)count; i++)
    {
        segment[i] = 0;
    }

    std::cout << segment[0] << std::endl;
    delete[] segment;
}

int main()
{
    build_segment();
    return 0;
}