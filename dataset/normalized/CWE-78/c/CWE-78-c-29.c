#include <wchar.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>
#include <winsock2.h>
#include <windows.h>

#pragma comment(lib, "ws2_32")

#define CLOSE_SOCKET closesocket
#define INVALID_SOCKET_VAL INVALID_SOCKET
#define SOCKET_ERROR_VAL SOCKET_ERROR

#define TCP_PORT 27015
#define LISTEN_BACKLOG 5

#define EXECV _wexecv

#define COMMAND_INT_PATH L"%WINDIR%\\system32\\cmd.exe"
#define COMMAND_ARG1 L"/c"
#define COMMAND_ARG2 L"findstr "

void wide_listen_socket_execv(void)
{
    wchar_t dataBuffer[100] = COMMAND_ARG2;
    wchar_t *data = dataBuffer;

    WSADATA wsaData;
    int wsaDataInit = 0;

    int recvResult;
    struct sockaddr_in service;
    wchar_t *replace;
    SOCKET listenSocket = INVALID_SOCKET_VAL;
    SOCKET acceptSocket = INVALID_SOCKET_VAL;
    size_t dataLen = wcslen(data);

    do
    {
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
            break;
        wsaDataInit = 1;

        listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (listenSocket == INVALID_SOCKET_VAL)
            break;

        memset(&service, 0, sizeof(service));
        service.sin_family = AF_INET;
        service.sin_addr.s_addr = INADDR_ANY;
        service.sin_port = htons(TCP_PORT);

        if (bind(listenSocket, (struct sockaddr *)&service, sizeof(service)) == SOCKET_ERROR_VAL)
            break;

        if (listen(listenSocket, LISTEN_BACKLOG) == SOCKET_ERROR_VAL)
            break;

        acceptSocket = accept(listenSocket, NULL, NULL);
        if (acceptSocket == SOCKET_ERROR_VAL)
            break;

        recvResult = recv(acceptSocket, (char *)(data + dataLen), (int)(sizeof(wchar_t) * (100 - dataLen - 1)), 0);
        if (recvResult == SOCKET_ERROR_VAL || recvResult == 0)
            break;

        data[dataLen + recvResult / (int)sizeof(wchar_t)] = L'\0';

        replace = wcschr(data, L'\r');
        if (replace)
            *replace = L'\0';
        replace = wcschr(data, L'\n');
        if (replace)
            *replace = L'\0';
    } while (0);

    if (listenSocket != INVALID_SOCKET_VAL)
        CLOSE_SOCKET(listenSocket);
    if (acceptSocket != INVALID_SOCKET_VAL)
        CLOSE_SOCKET(acceptSocket);

    if (wsaDataInit)
        WSACleanup();

    {
        wchar_t *args[] = { COMMAND_INT_PATH, COMMAND_ARG1, data, NULL };
        EXECV(COMMAND_INT_PATH, args);
    }
}