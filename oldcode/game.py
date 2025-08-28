from screeninfo import get_monitors
from window import WINDOW,ROOT
from objects import BIRD,PIPE
import tkinter as tk

def get_primary_monitor():
    monitors=get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return monitors[0]

monitor=get_primary_monitor()
# print(f"Primary Monitor: {monitor.name}")
# print(f"Resolution: {monitor.width} x {monitor.height}")
# print(f"Position: ({monitor.x}, {monitor.y})")

root=ROOT()

pipes=[]
PIPE_WIDTH,PIPE_HEIGHT=100,400
PIPE_IMAGE='./assets/pipe.png'
def add_pipe():
    pipes.append(PIPE(monitor))

add_pipe()
def main():
    bird=BIRD(monitor)
    while True:
        try:            
            root.update()
            bird.move()
            
            for i in range(len(pipes)):
                x,y=pipes[i].get_position()
                if x==0:
                    pipes.pop(0)
                    add_pipe()
                x-=1
                pipes[i].move()

        except tk.TclError:
            break

if __name__=="__main__":
    main()

del root