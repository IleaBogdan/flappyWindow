import win32pipe
import win32file
import pywintypes
import time
import threading
import queue

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
            # timeout = 5000  # milliseconds
            # win32pipe.SetNamedPipeHandleState(
            #     handle, 
            #     win32pipe.PIPE_READMODE_MESSAGE, 
            #     None, 
            #     timeout
            # ) # setting read timeout

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

def pipe_reader_thread(handle, q, stop_event):
    while not stop_event.is_set():
        try:
            result, data = win32file.ReadFile(handle, 64*1024)
            q.put(data)
        except Exception as e:
            q.put(b"Err")
            break

def start_pipe_listener(handle):
    q = queue.Queue()
    stop_event = threading.Event()
    t = threading.Thread(target=pipe_reader_thread, args=(handle, q, stop_event), daemon=True)
    t.start()
    return q, stop_event

# Usage example in your main loop:
if __name__=="__main__":
    pipe_name = r'\\.\pipe\MyPipe'
    handle = init_pipe(pipe_name)
    print("Connected! Reading data...\n")

    q, stop_event = start_pipe_listener(handle)
    buffer = b""
    try:
        while True:
            try:
                data = q.get(timeout=1)  # Wait for data, or timeout after 1s
            except queue.Empty:
                continue
            print(data)
            if not data or data == "Err":
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if line:
                    print(line.decode("utf-8"))
    finally:
        stop_event.set()
