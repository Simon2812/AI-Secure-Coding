#include "std_testcase.h"

#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#define INVALID_SOCKET_FD INVALID_SOCKET
#define SOCKET_FD SOCKET
#define SOCKET_ERR SOCKET_ERROR
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET close
#define INVALID_SOCKET_FD -1
#define SOCKET_FD int
#define SOCKET_ERR -1
#endif

#ifdef _WIN32
#include <process.h>
#define EXECVP _execvp
#define SHELL_BIN "cmd.exe"
#define SHELL_ARG "/c"
#else
#define EXECVP execvp
#define SHELL_BIN "sh"
#define SHELL_ARG "-c"
#endif

#define PORT_NUM 27015
#define BACKLOG_NUM 5

void run_listen_socket(void)
{
    char *q;
    char qbuf[100] = "q=";
    q = qbuf;

#ifdef _WIN32
    WSADATA wsa;
    int wsa_ok = 0;
#endif
    int rcv;
    struct sockaddr_in addr;
    char *cut;
    SOCKET_FD s_listen = INVALID_SOCKET_FD;
    SOCKET_FD s_client = INVALID_SOCKET_FD;
    size_t n = strlen(q);

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2,2), &wsa) != NO_ERROR)
            break;
        wsa_ok = 1;
#endif
        s_listen = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (s_listen == INVALID_SOCKET_FD)
            break;

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(PORT_NUM);

        if (bind(s_listen, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERR)
            break;
        if (listen(s_listen, BACKLOG_NUM) == SOCKET_ERR)
            break;

        s_client = accept(s_listen, NULL, NULL);
        if (s_client == SOCKET_ERR)
            break;

        rcv = recv(s_client, (char *)(q + n), (int)(sizeof(qbuf) - n - 1), 0);
        if (rcv == SOCKET_ERR || rcv == 0)
            break;

        q[n + (size_t)rcv] = '\0';

        cut = strchr(q, '\r');
        if (cut) *cut = '\0';
        cut = strchr(q, '\n');
        if (cut) *cut = '\0';

    } while (0);

    if (s_listen != INVALID_SOCKET_FD)
        CLOSE_SOCKET(s_listen);
    if (s_client != INVALID_SOCKET_FD)
        CLOSE_SOCKET(s_client);
#ifdef _WIN32
    if (wsa_ok)
        WSACleanup();
#endif

    {
        const char *sel = q + 2;
        const char *cmd;

#ifdef _WIN32
        if (strcmp(sel, "u") == 0)
            cmd = "hostname";
        else if (strcmp(sel, "p") == 0)
            cmd = "ver";
        else
            cmd = "whoami";
#else
        if (strcmp(sel, "u") == 0)
            cmd = "uname -s";
        else if (strcmp(sel, "p") == 0)
            cmd = "pwd";
        else
            cmd = "id -u";
#endif

        char *av[] = { (char *)SHELL_BIN, (char *)SHELL_ARG, (char *)cmd, NULL };
        EXECVP(SHELL_BIN, av);
    }
}