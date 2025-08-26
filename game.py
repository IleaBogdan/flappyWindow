from screeninfo import get_monitors
from window import WINDOW

def get_primary_monitor():
    monitors=get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return monitors[0]

monitor=get_primary_monitor()
print(f"Primary Monitor: {monitor.name}")
print(f"Resolution: {monitor.width} x {monitor.height}")
print(f"Position: ({monitor.x}, {monitor.y})")

bird=WINDOW("Bird",False,False)
while True:
    bird.display()
    x,y=bird.get_position()
    width,height=bird.get_size()
    if x+width>monitor.width or y+height>monitor.height:
        break;
    x+=1 
    bird.move_to(x,y)
del bird