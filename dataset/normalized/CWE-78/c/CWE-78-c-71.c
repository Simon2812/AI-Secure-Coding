#include "std_testcase.h"

#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#include <process.h>
#pragma comment(lib, "ws2_32")
#define CLOSE_SOCKET closesocket
#define SOCK_FD SOCKET
#define SOCK_BAD INVALID_SOCKET
#define SOCK_ERR SOCKET_ERROR
#define EXECL _wexecl
#define BIN_PATH L"%WINDIR%\\system32\\cmd.exe"
#define ARG0 L"%WINDIR%\\system32\\cmd.exe"
#define ARG1 L"/c"
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET close
#define SOCK_FD int
#define SOCK_BAD (-1)
#define SOCK_ERR (-1)
#define BIN_PATH "/bin/sh"
#define ARG0 "sh"
#define ARG1 "-c"
#endif

#define PORT_NUM 27015
#define IP_STR "127.0.0.1"

void connect_socket(void)
{
#ifdef _WIN32
    wchar_t *p;
    wchar_t buf[100] = L"q=";
    p = buf;
#else
    char *p;
    char buf[100] = "q=";
    p = buf;
#endif

#ifdef _WIN32
    WSADATA wsa;
    int wsa_ok = 0;
#endif
    int rcv;
    struct sockaddr_in addr;
    SOCK_FD s = SOCK_BAD;

#ifdef _WIN32
    size_t n = wcslen(p);
#else
    size_t n = strlen(p);
#endif

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2,2), &wsa) != NO_ERROR)
            break;
        wsa_ok = 1;
#endif
        s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (s == SOCK_BAD)
            break;

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(IP_STR);
        addr.sin_port = htons(PORT_NUM);

        if (connect(s, (struct sockaddr*)&addr, sizeof(addr)) == SOCK_ERR)
            break;

#ifdef _WIN32
        rcv = recv(s, (char *)(p + n), (int)(sizeof(buf) - (n + 1)) * (int)sizeof(wchar_t), 0);
#else
        rcv = recv(s, (char *)(p + n), (int)(sizeof(buf) - n - 1), 0);
#endif
        if (rcv == SOCK_ERR || rcv == 0)
            break;

#ifdef _WIN32
        p[n + (size_t)rcv / sizeof(wchar_t)] = L'\0';
        {
            wchar_t *cut = wcschr(p, L'\r');
            if (cut) *cut = L'\0';
            cut = wcschr(p, L'\n');
            if (cut) *cut = L'\0';
        }
#else
        p[n + (size_t)rcv] = '\0';
        {
            char *cut = strchr(p, '\r');
            if (cut) *cut = '\0';
            cut = strchr(p, '\n');
            if (cut) *cut = '\0';
        }
#endif
    } while (0);

    if (s != SOCK_BAD)
        CLOSE_SOCKET(s);
#ifdef _WIN32
    if (wsa_ok)
        WSACleanup();
#endif

#ifdef _WIN32
    {
        const wchar_t *sel = p + 2;
        const wchar_t *cmd;

        if (wcscmp(sel, L"a") == 0)
            cmd = L"ver";
        else if (wcscmp(sel, L"b") == 0)
            cmd = L"hostname";
        else
            cmd = L"whoami";

        EXECL(BIN_PATH, ARG0, ARG1, cmd, NULL);
    }
#else
    {
        const char *sel = p + 2;
        const char *cmd;

        if (strcmp(sel, "a") == 0)
            cmd = "uname -s";
        else if (strcmp(sel, "b") == 0)
            cmd = "id -u";
        else
            cmd = "pwd";

        execl(BIN_PATH, ARG0, ARG1, cmd, (char *)NULL);
    }
#endif
}