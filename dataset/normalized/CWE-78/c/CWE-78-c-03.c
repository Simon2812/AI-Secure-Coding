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
#define CMD_PATH "%WINDIR%\\system32\\cmd.exe"
#define CMD_FLAG "/c"
#define BASE_CMD "type "
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
#define CMD_PATH "/bin/sh"
#define CMD_FLAG "-c"
#define BASE_CMD "cat "
#endif

#define REMOTE_IP "127.0.0.1"
#define REMOTE_PORT 27015

void run_remote_file_dump(void)
{
    char buffer[100] = BASE_CMD;
    size_t baseLen = strlen(buffer);

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

        nread = recv(sock, buffer + baseLen, (int)(sizeof(buffer) - baseLen - 1), 0);
        if (nread <= 0)
            break;

        buffer[baseLen + (size_t)nread] = '\0';

        p = strchr(buffer, '\r');
        if (p) *p = '\0';
        p = strchr(buffer, '\n');
        if (p) *p = '\0';

    } while (0);

    if (sock != INVALID_SOCK)
        CLOSE_SOCKET(sock);

#ifdef _WIN32
    if (wsaReady)
        WSACleanup();
#endif

#ifdef _WIN32
    {
        char *args[] = { CMD_PATH, CMD_FLAG, buffer, NULL };
        _spawnv(_P_WAIT, CMD_PATH, args);
    }
#else
    execl(CMD_PATH, CMD_PATH, CMD_FLAG, buffer, NULL);
#endif
}