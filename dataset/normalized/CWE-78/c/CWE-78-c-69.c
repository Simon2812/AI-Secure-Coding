#include "std_testcase.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define CLOSE_SOCKET close
#define SOCKET int
#endif

#define TCP_PORT 27015
#define LISTEN_BACKLOG 5

#ifdef _WIN32
#define SYSTEM system
#else
#define SYSTEM system
#endif

void run_listen_system_task(void)
{
    char recvBuf[100] = {0};

#ifdef _WIN32
    WSADATA wsaData;
    int wsaInit = 0;
#endif

    int recvResult;
    struct sockaddr_in service;
    char *cr;
    char *lf;
    SOCKET listenSocket = INVALID_SOCKET;
    SOCKET acceptSocket = INVALID_SOCKET;

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
            break;
        wsaInit = 1;
#endif
        listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (listenSocket == INVALID_SOCKET)
            break;

        memset(&service, 0, sizeof(service));
        service.sin_family = AF_INET;
        service.sin_addr.s_addr = INADDR_ANY;
        service.sin_port = htons(TCP_PORT);

        if (bind(listenSocket, (struct sockaddr *)&service, sizeof(service)) == SOCKET_ERROR)
            break;
        if (listen(listenSocket, LISTEN_BACKLOG) == SOCKET_ERROR)
            break;

        acceptSocket = accept(listenSocket, NULL, NULL);
        if (acceptSocket == SOCKET_ERROR)
            break;

        recvResult = recv(acceptSocket, recvBuf, (int)(sizeof(recvBuf) - 1), 0);
        if (recvResult == SOCKET_ERROR || recvResult == 0)
            break;

        recvBuf[recvResult] = '\0';

        cr = strchr(recvBuf, '\r');
        if (cr)
            *cr = '\0';
        lf = strchr(recvBuf, '\n');
        if (lf)
            *lf = '\0';
    }
    while (0);

    if (listenSocket != INVALID_SOCKET)
        CLOSE_SOCKET(listenSocket);
    if (acceptSocket != INVALID_SOCKET)
        CLOSE_SOCKET(acceptSocket);

#ifdef _WIN32
    if (wsaInit)
        WSACleanup();
#endif

#ifdef _WIN32
    if (SYSTEM("whoami") != 0)
    {
        printLine("command execution failed!");
        exit(1);
    }
#else
    if (SYSTEM("id") != 0)
    {
        printLine("command execution failed!");
        exit(1);
    }
#endif
}