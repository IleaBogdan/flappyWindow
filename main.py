# from receiver import init_pipe, start_pipe_listener
from keycatcher import KeyCatcher
from screeninfo import get_monitors
from multiprocessing import Process
from window import WINDOW,ROOT
from objects import PIPE,BIRD,ScoreWindow
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
    score=ScoreWindow(monitor)
    try:
        while True:
            root.update()
            for i in range(len(pipes)):
                x, y = pipes[i].get_position()
                pipes[i].move()
            if len(pipes) > 0:
                x, y = pipes[-1].get_position()
                if monitor.width*2/3-15<=x and x<=monitor.width*2/3:
                    add_pipe(pipes, monitor)
            else:
                add_pipe(pipes, monitor)
            x, y = pipes[0].get_position()
            if x <= 30:
                pipes.pop(0)
                score.increase()
            root.update()
            # try:
            #     data = q.get(timeout=0.1)
            # except Exception:
            #     data = None
            # if data:
            #     print(data)
            #     if data == b"Err": break
            #     if data == b" ":
            #         bird.jump()
            
            jumped=False
            key = kc.check(timeout=0.03) 
            if key is not None:
                print(key)
                if key=='space':
                    bird.jump()
                    root.update()
                    jumped=True
                elif key=='esc':
                    break
            if not jumped:
                bird.move()
            #bird.on_top()


            exit_game=False
            bx,by=bird.get_position()
            bx+=BIRD.BIRD_WIDTH
            for i in range(len(pipes)):
                x,y=pipes[i].get_position()
                rx,ry=pipes[i].get_rposition()
                ry+=PIPE.PIPE_HEIGHT


                # if i==0: print(rx,ry,"----",bx,by)
                if by<ry and (rx<bx and bx<rx+PIPE.PIPE_WIDTH):
                    print("game over")
                    exit_game=True
                    break
                if y<by and (x<bx and bx<x+PIPE.PIPE_WIDTH):
                    print("game over")
                    exit_game=True
                    break

            if exit_game: break
            score.on_top()
            root.update()
    except tk.TclError:
        pass
    finally:
        # stop_event.set()
        del root

if __name__=="__main__":
    main()