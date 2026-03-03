#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#define SYSTEM _wsystem
#define FULL_COMMAND L"whoami "
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET close
#define SYSTEM system
#define FULL_COMMAND L"id "
#define SOCKET int
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#endif

#define TCP_PORT 27015
#define IP_ADDRESS "127.0.0.1"

void run_connect_socket_wide(void)
{
    wchar_t data_buf[100] = FULL_COMMAND;
    wchar_t *data = data_buf;

#ifdef _WIN32
    WSADATA wsaData;
    int wsaReady = 0;
#endif

    int recvResult;
    struct sockaddr_in service;
    wchar_t *replace;
    SOCKET connectSocket = INVALID_SOCKET;
    size_t dataLen = wcslen(data);

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0)
            break;
        wsaReady = 1;
#endif

        connectSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (connectSocket == INVALID_SOCKET)
            break;

        memset(&service, 0, sizeof(service));
        service.sin_family = AF_INET;
        service.sin_addr.s_addr = inet_addr(IP_ADDRESS);
        service.sin_port = htons(TCP_PORT);

        if (connect(connectSocket, (struct sockaddr*)&service, sizeof(service)) == SOCKET_ERROR)
            break;

        recvResult = recv(connectSocket,
                          (char *)(data + dataLen),
                          (int)(sizeof(wchar_t) * (100 - dataLen - 1)),
                          0);

        if (recvResult == SOCKET_ERROR || recvResult == 0)
            break;

        data[dataLen + recvResult / sizeof(wchar_t)] = L'\0';

        replace = wcschr(data, L'\r');
        if (replace) *replace = L'\0';
        replace = wcschr(data, L'\n');
        if (replace) *replace = L'\0';

    } while (0);

    if (connectSocket != INVALID_SOCKET)
        CLOSE_SOCKET(connectSocket);

#ifdef _WIN32
    if (wsaReady)
        WSACleanup();
#endif

    if (SYSTEM(data) != 0)
        exit(1);
}