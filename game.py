from screeninfo import get_monitors
from window import WINDOW,ROOT
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
    pipes.append(WINDOW(monitor,"Pipe",False,False,PIPE_IMAGE,PIPE_WIDTH,PIPE_HEIGHT,monitor.width-PIPE_WIDTH-100,monitor.height-PIPE_HEIGHT))

add_pipe()
def main():
    bird=WINDOW(monitor,"Bird",False,False,".\\assets\\bird.png",200,200)
    while True:
        try:            
            # bird.display()
            root.update()
            x,y=bird.get_position()
            x+=1 
            bird.move_to(x,y)

            i=0
            for i in range(len(pipes)):
                x,y=pipes[i].get_position()
                if x==0:
                    pipes[i].close()
                    pipes[i]=WINDOW(monitor,"Pipe",False,False,PIPE_IMAGE,PIPE_WIDTH,PIPE_HEIGHT,monitor.width-PIPE_WIDTH-100,monitor.height-PIPE_HEIGHT)
                x-=1
                pipes[i].move_to(x,y)

        except tk.TclError:
            break

if __name__=="__main__":
    main()

del root