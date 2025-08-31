import tkinter as tk
from PIL import Image, ImageTk # pyright: ignore[reportMissingImports]

class ROOT:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
    
    def __del__(self):
        self.root.destroy()
        # print("Root destroyed")
    
    def update(self):
        self.root.update()
        self.root.update_idletasks()

class WINDOW:
    def __init__(self, monitor, title="Title", resize_x=True, resize_y=True, 
                 imagePath=None, width=300, height=300, x=None, y=None,
                 always_on_top=False):
        self.monitor = monitor
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.resizable(resize_x, resize_y)
        self.name = title

        if x is not None and y is not None:
            self.window.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.window.geometry(f"{width}x{height}")
        
        if always_on_top:
            self.window.attributes('-topmost',True)

        self.photo = None    
        if imagePath:
            self.load_scaled_image(imagePath, width, height)
        
        # Bind window close event to ensure proper cleanup
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.window.update()
        self._closed = False
    
    def on_close(self):
        self._closed = True
        self.window.destroy()
        # print(f"{self.name} closed by user")
    
    # def __del__(self):
    #     """Destructor - ensures window is destroyed when object is garbage collected"""
    #     if not self._closed and self.window.winfo_exists():
    #         self.window.destroy()
    #         print(f"{self.name} deleted and window destroyed")
    #     else:
    #         print(f"{self.name} deleted (window already closed)")
    
    def display(self):
        if not self._closed:
            self.window.update()
    
    def move_to(self, x, y):
        if self._closed:
            return
            
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        if (x < self.monitor.x or y < self.monitor.y or 
            x + width > self.monitor.width or y + height > self.monitor.height):
            return
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def get_position(self):
        if self._closed:
            return None, None
        return self.window.winfo_x(), self.window.winfo_y()
    
    def get_size(self):
        if self._closed:
            return None, None
        return self.window.winfo_width(), self.window.winfo_height()
    
    def load_scaled_image(self, imagePath, width, height, scale_height_only=False, margin=2):
        try:
            image = Image.open(imagePath)
            if scale_height_only:
                new_height = int(height) - 2 * margin
                new_size = (image.width, new_height)
            else:
                ratio = min(width/image.width, height/image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
            resized = image.resize(new_size, Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized)
            # Use Canvas to control placement
            canvas = tk.Canvas(self.window, width=width, height=height, highlightthickness=0)
            canvas.pack()
            x = (width - new_size[0]) // 2
            y = margin
            canvas.create_image(x, y, anchor='nw', image=self.photo)
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def close(self):
        """Manually close the window"""
        if not self._closed:
            self._closed = True
            self.window.destroy()
            # print(f"{self.name} manually closed")
    def keep_on_top(self):
        self.window.attributes('-topmost',True)

# Example usage
if __name__ == "__main__":
    # Create root instance
    root = ROOT()
    
    # Create a mock monitor object with bounds
    class MockMonitor:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.width = 1920
            self.height = 1080
    
    monitor = MockMonitor()
    
    # Create windows
    windows = []
    for i in range(3):
        window = WINDOW(
            monitor=monitor,
            title=f"Test Window {i}",
            resize_x=False,
            resize_y=False,
            width=300,
            height=200,
            x=100 + i * 350,  # Position them horizontally
            y=100
        )
        windows.append(window)
    
    # Update root to keep things running
    root.update()
    
    # Simulate some activity
    import time
    time.sleep(2)
    
    # Delete one window - this should make it disappear from screen
    print("Deleting window 0...")
    del windows[0]  # This should trigger __del__ and destroy the window
    
    time.sleep(2)
    
    # Manually close another window
    print("Closing window 1 manually...")
    windows[0].close()  # Manual close
    
    time.sleep(2)
    
    # The remaining window should still be visible
    print("Remaining windows should still be visible...")
    
    # Keep the root updated
    try:
        while True:
            root.update()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    
    # Clean up remaining windows
    for window in windows:
        if hasattr(window, 'close'):
            window.close()