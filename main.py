from receiver import init_pipe,read_pipe
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

def gameloop():
    time.sleep(1)
    pipe_name = r'\\.\pipe\MyPipe'
    try:
        handle=init_pipe(pipe_name)
    except Exception as e:
        print(e)
        return
    buffer=b""

    monitor=get_primary_monitor()
    # print(f"Primary Monitor: {monitor.name}")
    print(f"Resolution: {monitor.width} x {monitor.height}")
    # print(f"Position: ({monitor.x}, {monitor.y})")

    root=ROOT()
    
    pipes=[]
    add_pipe(pipes,monitor)

    bird=BIRD(monitor)

    while True:
        try:
            root.update()

            for i in range(len(pipes)):
                x,y=pipes[i].get_position()
                pipes[i].move()
            if len(pipes)>0:
                x,y=pipes[-1].get_position()
                if x==monitor.width/2+100:
                    add_pipe(pipes,monitor)
            else: add_pipe(pipes,monitor)
            x,y=pipes[0].get_position()
            if x==0:
                pipes.pop(0)
            
            data=read_pipe(handle)
            if data:
                bird.move()
                bird.on_top()
                if data=="TLE": continue
                if data=="Err": break
                buffer+=data
                while b"\n" in buffer:
                    line,buffer=buffer.split(b"\n",1)
                    if line:
                        print(line)
        except tk.TclError:
            break
    del root
    

def main():
    exe_procces=multiprocessing.Process(target=catch_keys)
    exe_procces.start()
    gameloop()

if __name__=="__main__":
    main()