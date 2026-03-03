#include "std_testcase.h"
#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define FULL_COMMAND "tasklist "
#else
#include <unistd.h>
#define FULL_COMMAND "id "
#endif

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
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define CLOSE_SOCKET close
#define SOCKET int
#endif

#define TCP_PORT 27015
#define IP_ADDRESS "127.0.0.1"

#ifdef _WIN32
#define POPEN _popen
#define PCLOSE _pclose
#else
#define POPEN popen
#define PCLOSE pclose
#endif

void run_client_query(void)
{
    char buf[100] = FULL_COMMAND;
    char *out = buf;

#ifdef _WIN32
    WSADATA wsaData;
    int wsaDataInit = 0;
#endif
    int recvResult;
    struct sockaddr_in service;
    char *replace;
    SOCKET s = INVALID_SOCKET;
    size_t len = strlen(out);

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
            break;
        wsaDataInit = 1;
#endif
        s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (s == INVALID_SOCKET)
            break;

        memset(&service, 0, sizeof(service));
        service.sin_family = AF_INET;
        service.sin_addr.s_addr = inet_addr(IP_ADDRESS);
        service.sin_port = htons(TCP_PORT);

        if (connect(s, (struct sockaddr *)&service, sizeof(service)) == SOCKET_ERROR)
            break;

        recvResult = recv(s, (char *)(out + len), (int)(sizeof(char) * (100 - len - 1)), 0);
        if (recvResult == SOCKET_ERROR || recvResult == 0)
            break;

        out[len + recvResult / (int)sizeof(char)] = '\0';

        replace = strchr(out, '\r');
        if (replace)
            *replace = '\0';
        replace = strchr(out, '\n');
        if (replace)
            *replace = '\0';
    } while (0);

    if (s != INVALID_SOCKET)
        CLOSE_SOCKET(s);

#ifdef _WIN32
    if (wsaDataInit)
        WSACleanup();
#endif

    {
        FILE *pipe;
#ifdef _WIN32
        pipe = POPEN("tasklist", "r");
#else
        pipe = POPEN("id", "r");
#endif
        if (pipe != NULL)
            PCLOSE(pipe);
    }
}