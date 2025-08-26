import tkinter as tk

class WINDOW:
    def __init__(self, title="Title"):
        self.window=tk.Tk()
        self.window.wm_title(title)
    def display(self):
        self.window.update()
    def move_to(self,x,y):
        width=self.window.winfo_width()
        height=self.window.winfo_height()
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    def get_position(self):
        return self.window.winfo_x(),self.window.winfo_y()

if __name__=="__main__":
    w=WINDOW("Test")

    while True:
        w.display()
        x,y=w.get_position()
        x+=1 # only int movement allowed
        w.move_to(x,y)
