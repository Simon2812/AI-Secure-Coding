#include "std_testcase.h"

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#include <direct.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define CLOSE_SOCKET close
#define SOCKET int
#endif

#include <math.h>
#include <limits.h>

#define TCP_PORT 27015
#define LISTEN_BACKLOG 5

static int receive_value()
{
    int value = 0;

#ifdef _WIN32
    WSADATA wsaData;
    int initialized = 0;
#endif

    SOCKET srv = INVALID_SOCKET;
    SOCKET cli = INVALID_SOCKET;
    struct sockaddr_in addr;
    char buffer[32];

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2,2), &wsaData) != NO_ERROR)
            break;
        initialized = 1;
#endif

        srv = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (srv == INVALID_SOCKET)
            break;

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(TCP_PORT);

        if (bind(srv, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR)
            break;

        if (listen(srv, LISTEN_BACKLOG) == SOCKET_ERROR)
            break;

        cli = accept(srv, NULL, NULL);
        if (cli == SOCKET_ERROR)
            break;

        int received = recv(cli, buffer, sizeof(buffer) - 1, 0);
        if (received <= 0)
            break;

        buffer[received] = '\0';
        value = atoi(buffer);

    } while (0);

    if (srv != INVALID_SOCKET)
        CLOSE_SOCKET(srv);
    if (cli != INVALID_SOCKET)
        CLOSE_SOCKET(cli);

#ifdef _WIN32
    if (initialized)
        WSACleanup();
#endif

    return value;
}

int main(void)
{
    int x = receive_value();

    if (x > INT_MIN && abs(x) <= (int)sqrt((double)INT_MAX))
    {
        int squared = x * x;
        printIntLine(squared);
    }
    else
    {
        printLine("input out of safe range");
    }

    return 0;
}