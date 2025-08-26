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


def main():
    bird=WINDOW("Bird",False,False,".\\assets\\bird.png",200,200)
    bird2=WINDOW("Bird2",False,False,".\\assets\\bird.png",200,200)
    db1,db2=False,False
    while True:
        try:            
            # bird.display()
            root.update()

            if not db1:
                x,y=bird.get_position()
                width,height=bird.get_size()
                if x+width>monitor.width or y+height>monitor.height:
                    del bird
                    db1=True
                else:
                    x+=1 
                    bird.move_to(x,y)

            if not db2:
                x,y=bird2.get_position()
                width,height=bird2.get_size()
                if x+width>monitor.width or y+height>monitor.height:
                    del bird2
                    db2=True
                else:
                    y+=1 
                    bird2.move_to(x,y)
            if db1 and db2:
                break
        
        except tk.TclError:
            break
    if not db1:del bird
    if not db2:del bird2

if __name__=="__main__":
    main()

del root