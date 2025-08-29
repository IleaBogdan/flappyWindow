import win32pipe, win32file, pywintypes
import time

pipe_name = r'\\.\pipe\MyPipe'

print("Waiting for pipe...")

while True:
    try:
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )
        break  # success
    except pywintypes.error as e:
        if e.args[0] == 2:  # ERROR_FILE_NOT_FOUND
            time.sleep(1)   # wait and retry
        else:
            raise

print("Connected! Reading numbers...\n")

buffer = b""
while True:
    try:
        result, data = win32file.ReadFile(handle, 64*1024)
    except Exception:
        break  # pipe closed

    if not data:
        break
    buffer += data
    while b"\n" in buffer:
        line, buffer = buffer.split(b"\n", 1)
        if line:
            print(line.decode("utf-8"))
