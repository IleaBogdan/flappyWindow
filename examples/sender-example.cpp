#include <windows.h>
#include <iostream>
#include <string>

int main() {
    const char* pipeName = R"(\\.\pipe\MyPipe)";

    // Create the named pipe
    HANDLE hPipe = CreateNamedPipeA(
        pipeName,
        PIPE_ACCESS_OUTBOUND,               // write only
        PIPE_TYPE_BYTE | PIPE_WAIT,
        1, 0, 0, 0, NULL
    );

    if (hPipe == INVALID_HANDLE_VALUE) {
        std::cerr << "CreateNamedPipe failed. Error: " << GetLastError() << std::endl;
        return 1;
    }

    std::cout << "Waiting for Python to connect...\n";
    ConnectNamedPipe(hPipe, NULL);
    std::cout << "Connected! Sending numbers...\n";

    DWORD written;
    for (int i = 1; i <= 100; i++) {
        std::string msg = std::to_string(i) + "\n"; // send each number + newline
        WriteFile(hPipe, msg.c_str(), (DWORD)msg.size(), &written, NULL);
    }

    std::cout << "Done.\n";
    CloseHandle(hPipe);
    return 0;
}
