#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#include <process.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#define SOCKET_TYPE SOCKET
#define INVALID_SOCK INVALID_SOCKET
#define SOCKERR SOCKET_ERROR
#define SHELL_PATH "%WINDIR%\\system32\\cmd.exe"
#define SHELL_NAME "cmd.exe"
#define SHELL_FLAG "/c"
#define PREFIX_CMD "ping -n 1 "
#define RUN_EXECL _execl
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
#define SHELL_PATH "/bin/sh"
#define SHELL_NAME "sh"
#define SHELL_FLAG "-c"
#define PREFIX_CMD "ping -c 1 "
#define RUN_EXECL execl
#endif

#define REMOTE_IP "127.0.0.1"
#define REMOTE_PORT 27015

void remote_probe(void)
{
    char cmd[100] = PREFIX_CMD;
    size_t cmdLen = strlen(cmd);

#ifdef _WIN32
    WSADATA wsaData;
    int wsaReady = 0;
#endif

    SOCKET_TYPE sock = INVALID_SOCK;
    struct sockaddr_in addr;
    int nread;
    char *p;

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
            break;
        wsaReady = 1;
#endif

        sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (sock == INVALID_SOCK)
            break;

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(REMOTE_IP);
        addr.sin_port = htons(REMOTE_PORT);

        if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) == SOCKERR)
            break;

        nread = recv(sock, cmd + cmdLen, (int)(sizeof(cmd) - cmdLen - 1), 0);
        if (nread <= 0)
            break;

        cmd[cmdLen + (size_t)nread] = '\0';

        p = strchr(cmd, '\r');
        if (p) *p = '\0';
        p = strchr(cmd, '\n');
        if (p) *p = '\0';

    } while (0);

    if (sock != INVALID_SOCK)
        CLOSE_SOCKET(sock);

#ifdef _WIN32
    if (wsaReady)
        WSACleanup();
#endif

    RUN_EXECL(SHELL_PATH, SHELL_NAME, SHELL_FLAG, cmd, NULL);
}