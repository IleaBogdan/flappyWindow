from window import WINDOW

class BIRD:
    BIRD_IMAGE=".\\assets\\bird.png"
    MOVE_SET=10
    def __init__(self,monitor):
        self.window=WINDOW(monitor,"Bird",False,False,BIRD.BIRD_IMAGE,200,200,100,monitor.height//2,True)
    def __del__(delf):
        # print("You killed the bird")
        pass
    def move(self):
        print("move bird move")
        x,y=self.window.get_position()
        y+=BIRD.MOVE_SET
        self.window.move_to(x,y)
    def jump(self):
        x,y=self.window.get_position()
        y-=3*BIRD.MOVE_SET
        self.window.move_to(x,y)
    def on_top(self):
        self.window.keep_on_top()

class PIPE:
    PIPE_WIDTH,PIPE_HEIGHT=100,400
    PIPE_IMAGE='./assets/pipe.png'
    MOVE_SET=10
    def __init__(self,monitor):
        self.window=WINDOW(monitor,"Pipe",False,False,PIPE.PIPE_IMAGE,PIPE.PIPE_WIDTH,PIPE.PIPE_HEIGHT,monitor.width-PIPE.PIPE_WIDTH-100,monitor.height-PIPE.PIPE_HEIGHT,True)
    def __del__(self):
        try:
            self.window.close()
        except Exception as e:
            print(e)
    def move(self):
        x,y=self.window.get_position()
        x-=PIPE.MOVE_SET
        self.window.move_to(x,y)
    def get_position(self):
        return self.window.get_position()    