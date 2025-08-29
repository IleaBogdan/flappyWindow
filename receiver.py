import win32pipe
import win32file
import pywintypes
import time

def init_pipe(pipe_name):
    ok=False
    for i in range(10):
        print(f"Try: {i}")
        try:
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ,
                0, None,
                win32file.OPEN_EXISTING,
                0, None
            )
            ok=True
            print("Success")
            break  # success
        except pywintypes.error as e:
            print("Failed")
            if e.args[0] == 2:  # ERROR_FILE_NOT_FOUND
                time.sleep(1)   # wait and retry
            else:
                raise
    if not ok: raise("couldn't connect to pipe")
    return handle 

def read_pipe(pipe_name):
    try:
        result, data = win32file.ReadFile(handle, 64*1024)
    except Exception:
        return None
    return data
        

if __name__=="__main__":
    pipe_name = r'\\.\pipe\MyPipe'
    handle=init_pipe(pipe_name)
    print("Connected! Reading numbers...\n")

    buffer = b""
    while True:
        data=read_pipe(pipe_name)
        if not data:
            break
        
        print(data)
        buffer += data
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            if line:
                print(line.decode("utf-8"))
