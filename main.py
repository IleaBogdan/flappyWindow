# from receiver import init_pipe, start_pipe_listener
from keycatcher import KeyCatcher
from screeninfo import get_monitors
from multiprocessing import Process
from window import WINDOW,ROOT
from objects import PIPE,BIRD
import multiprocessing
import tkinter as tk
import subprocess
import threading
import time
import os

def get_primary_monitor():
    monitors=get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return monitors[0]

def add_pipe(pipes,monitor):
    pipes.append(PIPE(monitor))

def catch_keys():
    # os.system('.\\bin\\keycatcher.exe') # running the keycatcher exe to start the pipe
    # subprocess.Popen(['.\\bin\\keycatcher.exe'])
    subprocess.run(['.\\bin\\keycatcher.exe'])
    print("running exe")


def main():
    # time.sleep(1)
    # pipe_name = r'\\.\pipe\MyPipe'
    # try:
    #     handle = init_pipe(pipe_name)
    #     q, stop_event = start_pipe_listener(handle)
    # except Exception as e:
    #     print(e)
    #     return
    # buffer = b""
    kc=KeyCatcher(suppress=True)

    monitor = get_primary_monitor()
    print(f"Resolution: {monitor.width} x {monitor.height}")

    root = ROOT()
    pipes = []
    add_pipe(pipes, monitor)
    bird = BIRD(monitor)

    try:
        while True:
            root.update()
            for i in range(len(pipes)):
                x, y = pipes[i].get_position()
                pipes[i].move()
            if len(pipes) > 0:
                x, y = pipes[-1].get_position()
                if x == monitor.width / 2 + 100:
                    add_pipe(pipes, monitor)
            else:
                add_pipe(pipes, monitor)
            x, y = pipes[0].get_position()
            if x <= 30:
                pipes.pop(0)

            # try:
            #     data = q.get(timeout=0.1)
            # except Exception:
            #     data = None

            bird.move()
            bird.on_top()
            # if data:
            #     print(data)
            #     if data == b"Err": break
            #     if data == b" ":
            #         bird.jump()
            key = kc.check(timeout=0.1) 
            if key is not None:
                print(key)
                if key=='space':
                    bird.jump()
                elif key=='esc':
                    break
    except tk.TclError:
        pass
    finally:
        # stop_event.set()
        del root

if __name__=="__main__":
    main()