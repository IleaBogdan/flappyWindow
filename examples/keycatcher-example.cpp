#include <Windows.h>
#include <iostream>
#include <fstream>

using namespace std;


HHOOK hHook=NULL;

#ifdef LOGFILE
    ofstream fout("keycatcher.txt");
#endif

LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam){
    if (nCode>=0){
        KBDLLHOOKSTRUCT* pKey=(KBDLLHOOKSTRUCT*)lParam;
        
        if (wParam==WM_KEYDOWN || wParam==WM_SYSKEYDOWN){
            #ifdef LOGFILE
                fout<<"Key pressed: "<<pKey->vkCode<<endl;
            #endif
            
            if (pKey->vkCode==VK_ESCAPE){ // Exit on Escape
                #ifdef LOGFILE
                    fout<<"Exit requested"<<endl;
                #endif
                PostQuitMessage(0);
                return 1;
            }
        }
    }
    #ifdef LOGFILE
        fout<<"Key blocked!"<<endl;
    #endif
    return 1;
    // return CallNextHookEx(hHook, nCode, wParam, lParam);
}

// Window procedure for hidden window
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
    
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0) > 0){
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    // Cleanup
    UnhookWindowsHookEx(hHook);
    #ifdef LOGFILE
        fout<<"Hook uninstalled, exiting..."<<endl;
        fout.close();
    #endif
    
    return 0;
}