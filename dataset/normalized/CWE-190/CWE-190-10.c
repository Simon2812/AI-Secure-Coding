#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#define CLOSE_SOCKET close
#define SOCKET int
#define INVALID_SOCKET -1
#endif

#define PORT 27015

static int read_metric()
{
    int metric = 0;
    SOCKET s = INVALID_SOCKET;
    struct sockaddr_in addr;
    char buf[32];

#ifdef _WIN32
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);
#endif

    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s == INVALID_SOCKET)
        return 0;

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(s, (struct sockaddr*)&addr, sizeof(addr)) == 0)
    {
        int n = recv(s, buf, sizeof(buf) - 1, 0);
        if (n > 0)
        {
            buf[n] = '\0';
            metric = atoi(buf);
        }
    }

    CLOSE_SOCKET(s);
#ifdef _WIN32
    WSACleanup();
#endif

    return metric;
}

int main(void)
{
    int base = read_metric();

    if (base > 0)
    {
        int doubled = base * 2;
        printf("%d\n", doubled);
    }

    return 0;
}