#include "std_testcase.h"

#include <wchar.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#define BASE_W L"dir "
#else
#include <unistd.h>
#define BASE_W L"ls "
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
#define OPEN_PIPE _wpopen
#define CLOSE_PIPE _pclose
#else
#define OPEN_PIPE popen
#define CLOSE_PIPE pclose
#endif

void run_socket_connect(void)
{
    wchar_t *p;
    wchar_t wbuf[100] = BASE_W;
    p = wbuf;

#ifdef _WIN32
    WSADATA wsaData;
    int wsaInit = 0;
#endif
    int rcv;
    struct sockaddr_in svc;
    wchar_t *cut;
    SOCKET s = INVALID_SOCKET;
    size_t baseLen = wcslen(p);

    do
    {
#ifdef _WIN32
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != NO_ERROR)
        {
            break;
        }
        wsaInit = 1;
#endif
        s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (s == INVALID_SOCKET)
        {
            break;
        }

        memset(&svc, 0, sizeof(svc));
        svc.sin_family = AF_INET;
        svc.sin_addr.s_addr = inet_addr(IP_ADDRESS);
        svc.sin_port = htons(TCP_PORT);

        if (connect(s, (struct sockaddr *)&svc, sizeof(svc)) == SOCKET_ERROR)
        {
            break;
        }

        rcv = recv(s, (char *)(p + baseLen), (int)(sizeof(wbuf) - baseLen - 1) * (int)sizeof(wchar_t), 0);
        if (rcv == SOCKET_ERROR || rcv == 0)
        {
            break;
        }

        p[baseLen + (size_t)rcv / sizeof(wchar_t)] = L'\0';

        cut = wcschr(p, L'\r');
        if (cut) *cut = L'\0';
        cut = wcschr(p, L'\n');
        if (cut) *cut = L'\0';
    }
    while (0);

    if (s != INVALID_SOCKET)
    {
        CLOSE_SOCKET(s);
    }
#ifdef _WIN32
    if (wsaInit)
    {
        WSACleanup();
    }
#endif

    {
        const wchar_t *token = p + wcslen(BASE_W);

#ifdef _WIN32
        const wchar_t *cmdW = L"dir";
        if (wcscmp(token, L"me") == 0)
        {
            cmdW = L"whoami";
        }
        else if (wcscmp(token, L"ver") == 0)
        {
            cmdW = L"ver";
        }

        {
            wchar_t finalW[100];
            _snwprintf(finalW, 99, L"%s", cmdW);
            finalW[99] = L'\0';

            FILE *fp = OPEN_PIPE(finalW, L"w");
            if (fp != NULL)
            {
                CLOSE_PIPE(fp);
            }
        }
#else
        const char *cmdA = "ls";
        if (wcscmp(token, L"me") == 0)
        {
            cmdA = "id";
        }
        else if (wcscmp(token, L"ver") == 0)
        {
            cmdA = "uname -a";
        }

        {
            FILE *fp = OPEN_PIPE(cmdA, "w");
            if (fp != NULL)
            {
                CLOSE_PIPE(fp);
            }
        }
#endif
    }
}