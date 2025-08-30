from window import WINDOW
import tkinter as tk

class BIRD:
    BIRD_IMAGE=".\\assets\\bird.png"
    MOVE_SET=3
    BIRD_WIDTH,BIRD_HEIGHT=200,200
    def __init__(self,monitor):
        self.window=WINDOW(monitor,"Bird",False,False,BIRD.BIRD_IMAGE,BIRD.BIRD_WIDTH,BIRD.BIRD_HEIGHT,200,monitor.height//2,True)
    def __del__(delf):
        # print("You killed the bird")
        pass
    def move(self):
        #print("move bird move")
        x,y=self.window.get_position()
        y+=BIRD.MOVE_SET
        self.window.move_to(x,y)
    def jump(self):
        x,y=self.window.get_position()
        y-=7*BIRD.MOVE_SET
        self.window.move_to(x,y)
    def on_top(self):
        self.window.keep_on_top()
    def get_position(self):
        return self.window.get_position()

class PIPE:
    PIPE_WIDTH,PIPE_HEIGHT=100,300
    PIPE_IMAGE='./assets/pipe.png'
    PIPE_RIMAGE='./assets/rpipe.png'
    MOVE_SET=6
    def __init__(self,monitor):
        self.window=WINDOW(monitor,"Pipe",False,False,None,PIPE.PIPE_WIDTH,PIPE.PIPE_HEIGHT,monitor.width-PIPE.PIPE_WIDTH-60,monitor.height-PIPE.PIPE_HEIGHT,True)
        self.window.load_scaled_image(PIPE.PIPE_IMAGE, PIPE.PIPE_WIDTH, PIPE.PIPE_HEIGHT, scale_height_only=True, margin=2)
        self.rwindow=WINDOW(monitor,"Pipe",False,False,None,PIPE.PIPE_WIDTH,PIPE.PIPE_HEIGHT,monitor.width-PIPE.PIPE_WIDTH-60,0,True)
        self.rwindow.load_scaled_image(PIPE.PIPE_RIMAGE, PIPE.PIPE_WIDTH, PIPE.PIPE_HEIGHT, scale_height_only=True, margin=2)
    def __del__(self):
        try:
            self.window.close()
            self.rwindow.close()
        except Exception as e:
            print(e)
    def move(self):
        x,y=self.window.get_position()
        x-=PIPE.MOVE_SET
        self.window.move_to(x,y)
        x,y=self.rwindow.get_position()
        x-=PIPE.MOVE_SET
        self.rwindow.move_to(x,y)
    def get_position(self):
        return self.window.get_position()
    def get_rposition(self):
        return self.rwindow.get_position()
    

class ScoreWindow:
    def __init__(self,monitor):
        WIDTH=200
        self.window=WINDOW(monitor,"Score",False,False,None,WIDTH,50,monitor.width-WIDTH-100,50,True)
        self.label=tk.Message(self.window.window,text="Score 0",width=WIDTH,font=("Arial",12))
        self.label.pack(pady=10)
        self.score=0
    def __del__(self):
        self.window.close()
    def increase(self):
        self.score+=1
        self.label.config(text=f"Score: {self.score}")
    def on_top(self):
        self.window.keep_on_top()