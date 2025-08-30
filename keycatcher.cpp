#include<Windows.h>
#include<windows.h>
#include<unordered_map>
#include<cstdint>
#ifdef LOGFILE
    #include<fstream>
#endif
using namespace std;

#ifdef LOGFILE
    ofstream fout("keycatcher.txt");
#endif

const unordered_map<DWORD,string>key_mapper={
    {0x20," "},
    {0x1B,"ESC"},
};
HHOOK hHook=nullptr;
HANDLE hPipe;
DWORD written;
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam){
    if (nCode>=0){
        KBDLLHOOKSTRUCT* pKey=(KBDLLHOOKSTRUCT*)lParam;
        
        if (wParam==WM_KEYDOWN || wParam==WM_SYSKEYDOWN){
            if (key_mapper.count(pKey->vkCode)){
                #ifdef LOGFILE
                    // fout<<"Key pressed: "<<pKey->vkCode<<endl;
                    fout<<pKey->vkCode;
                    fout<<" - "<<key_mapper.at(pKey->vkCode)<<" - "<<key_mapper.count(pKey->vkCode)<<endl;
                #endif
                WriteFile(
                    hPipe,
                    key_mapper.at(pKey->vkCode).c_str(),
                    (DWORD)key_mapper.at(pKey->vkCode).size(),
                    &written,
                    nullptr
                );
            }
            if (pKey->vkCode==VK_ESCAPE){ // Exit on Escape
                PostQuitMessage(0);
                return 1;
            }
        }
    }
    return 1; // block keypassing
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam){
    switch (uMsg){
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_CLOSE:
        DestroyWindow(hwnd);
        return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow){
    // Create hidden window
    WNDCLASS wc={};
    wc.lpfnWndProc=WindowProc;
    wc.hInstance=hInstance;
    wc.lpszClassName="KeyInterceptorClass";

    RegisterClass(&wc);
    
    HWND hwnd=CreateWindowEx(
        0,
        "KeyInterceptorClass", // fuck of vscode for giving me errors for const char *, it works with this one
        "Key Interceptor",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
        NULL, NULL, hInstance, NULL
    );
    
    if (!hwnd){
        return 1;
    }
    
    // Set the keyboard hook
    hHook=SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, NULL, 0);
    
    if (!hHook){
        #ifdef LOGFILE
            fout<<"Failed to set hook! Error: "<<GetLastError()<<endl;
        #endif
        return 1;
    }
    
    #ifdef LOGFILE
        fout<<"Keyboard hook installed successfully"<<endl;
    #endif

    const char* pipeName = R"(\\.\pipe\MyPipe)";
    // Create the named pipe
    hPipe = CreateNamedPipeA(
        pipeName,
        PIPE_ACCESS_OUTBOUND,               // write only
        PIPE_TYPE_BYTE | PIPE_WAIT,
        1, 0, 0, 0, NULL
    );

    if (hPipe == INVALID_HANDLE_VALUE) {
        #ifdef LOGFILE
            fout << "CreateNamedPipe failed. Error: " << GetLastError() << std::endl;
        #endif
        return 1;
    }
    ConnectNamedPipe(hPipe, NULL); // waiting for python to connect

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0) > 0){
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    // Cleanup
    UnhookWindowsHookEx(hHook);
    #ifdef LOGFILE
        fout<<"Hook uninstalled, exiting..."<<endl;
        //fout.close();
    #endif
    
    return 0;
}