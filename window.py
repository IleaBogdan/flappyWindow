import tkinter as tk

class WINDOW:
    def __init__(self, title="Title",resize_x=True,resize_y=True):
        self.window=tk.Tk()
        self.window.wm_title(title)
        self.window.resizable(resize_x,resize_y)
    def __del__(self):
        self.window.destroy()
    def display(self):
        self.window.update()
    def move_to(self,x,y):
        width=self.window.winfo_width()
        height=self.window.winfo_height()
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    def get_position(self):
        return self.window.winfo_x(),self.window.winfo_y()
    def get_size(self):
        return self.window.winfo_width(),self.window.winfo_height()

if __name__=="__main__":
    w=WINDOW("Test")

    while True:
        w.display()
        x,y=w.get_position()
        x+=1 # only int movement allowed
        w.move_to(x,y)
