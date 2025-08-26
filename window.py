import tkinter as tk
from PIL import Image, ImageTk

class ROOT:
    def __init__(self):
        self.root=tk.Tk()
        self.root.withdraw()
    def __del__(self):
        self.root.destroy()
    def update(self):
        self.root.update()
        self.root.update_idletasks()

class WINDOW:
    def __init__(self, title="Title",resize_x=True,resize_y=True,imagePath=None,width=300,height=300):
        self.window=tk.Toplevel()
        self.window.title(title)
        self.window.resizable(resize_x, resize_y)
        self.name=title
        self.window.geometry(f"{width}x{height}")
        self.photo=None
        if imagePath:
            self.load_scaled_image(imagePath, width, height)
        self.window.update() # no need for this anymore
        
    def __del__(self):
        # no need for specific destruction thanks to root destructor
        # self.window.destroy()
        print(f"{self.name} deleted")

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
    def load_scaled_image(self, imagePath, width, height):
        try:
            image = Image.open(imagePath)
            ratio = min(width/image.width, height/image.height) # Calculate scaling ratio while maintaining aspect ratio
            new_size = (int(image.width * ratio), int(image.height * ratio))
            resized = image.resize(new_size, Image.Resampling.LANCZOS) # Resize and convert to PhotoImage
            self.photo = ImageTk.PhotoImage(resized)
            tk.Label(self.window, image=self.photo).pack(expand=True)# Display the image
        except Exception as e:
            print(f"Error loading image: {e}")

if __name__=="__main__":
    w=WINDOW("Test",False,False,".\\assets\\test.png")

    while True:
        # w.display()
        x,y=w.get_position()
        x+=1 # only int movement allowed
        w.move_to(x,y)
