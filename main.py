from screeninfo import get_monitors
from libloader import load_libs
from window import WINDOW,ROOT
from objects import PIPE,BIRD
import tkinter as tk
import threading

def get_primary_monitor():
    monitors=get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return monitors[0]

def add_pipe(pipes,monitor):
    pipes.append(PIPE(monitor))

def main():
    libs=load_libs()
    # print(libs)
    
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
            
            bird.move()
            bird.on_top()
        except tk.TclError:
            break
    del root

if __name__=="__main__":
    main()