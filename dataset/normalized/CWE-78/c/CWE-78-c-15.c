#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#define SOCKET_TYPE SOCKET
#define INVALID_SOCK INVALID_SOCKET
#define SOCKERR SOCKET_ERROR
#include <process.h>
#define EXECVP _execvp
#define COMMAND_INT_PATH "%WINDIR%\\system32\\cmd.exe"
#define COMMAND_INT "cmd.exe"
#define COMMAND_ARG1 "/c"
#define COMMAND_ARG2 "where "
#define COMMAND_ARG3 data
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET close
#define SOCKET_TYPE int
#define INVALID_SOCK (-1)
#define SOCKERR (-1)
#include <process.h>
#define EXECVP execvp
#define COMMAND_INT_PATH "/bin/sh"
#define COMMAND_INT "sh"
#define COMMAND_ARG1 "-c"
#define COMMAND_ARG2 "stat "
#define COMMAND_ARG3 data
#endif

#define TCP_PORT 27015
#define LISTEN_BACKLOG 5

void run_listen_socket_lookup(void)
{
#ifdef _WIN32
    WSADATA wsaData;
    int wsaReady = 0;
#endif

    int recvResult;
    struct sockaddr_in service;
    char *replace;
    SOCKET_TYPE listenSocket = INVALID_SOCK;
    SOCKET_TYPE acceptSocket = INVALID_SOCK;

    char dataBuffer[100] = COMMAND_ARG2;
    char *data = dataBuffer;
    size_t dataLen = strlen(data);

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
            break;
        wsaReady = 1;
#endif

        listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (listenSocket == INVALID_SOCK)
            break;

        memset(&service, 0, sizeof(service));
        service.sin_family = AF_INET;
        service.sin_addr.s_addr = INADDR_ANY;
        service.sin_port = htons(TCP_PORT);

        if (bind(listenSocket, (struct sockaddr *)&service, sizeof(service)) == SOCKERR)
            break;

        if (listen(listenSocket, LISTEN_BACKLOG) == SOCKERR)
            break;

        acceptSocket = accept(listenSocket, NULL, NULL);
        if (acceptSocket == SOCKERR)
            break;

        recvResult = recv(acceptSocket, (char *)(data + dataLen),
                          (int)(sizeof(dataBuffer) - dataLen - 1), 0);
        if (recvResult == SOCKERR || recvResult == 0)
            break;

        data[dataLen + (size_t)recvResult] = '\0';

        replace = strchr(data, '\r');
        if (replace) *replace = '\0';
        replace = strchr(data, '\n');
        if (replace) *replace = '\0';

    } while (0);

    if (listenSocket != INVALID_SOCK)
        CLOSE_SOCKET(listenSocket);
    if (acceptSocket != INVALID_SOCK)
        CLOSE_SOCKET(acceptSocket);

#ifdef _WIN32
    if (wsaReady)
        WSACleanup();
#endif

    {
        char *args[] = { COMMAND_INT_PATH, COMMAND_ARG1, COMMAND_ARG3, NULL };
        EXECVP(COMMAND_INT, args);
    }
}