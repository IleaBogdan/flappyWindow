from pynput import keyboard
import time
import queue

class KeyCatcher:
    def __init__(self, suppress=True):
        self.should_exit = False
        self.suppress = suppress
        self.key_queue = queue.Queue()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            suppress=self.suppress
        )
        self.listener.start()

    def on_press(self, key):
        try:
            key_char = key.char
            self.key_queue.put(key_char)
            if key_char == 'esc':
                self.should_exit = True
                return False  # Stop listener
        except AttributeError:
            key_name = str(key).replace('Key.', '')
            self.key_queue.put(key_name)
            if key_name == 'esc':
                self.should_exit = True
                return False  # Stop listener

    def check(self, timeout=None):
        try:
            return self.key_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def __del__(self):
        self.listener.stop()

if __name__ == "__main__":
    kc = KeyCatcher(suppress=True)
    try:
        while not kc.should_exit:
            key = kc.check(timeout=0.1)  # Wait up to 0.1s for a key
            if key is not None:
                print(key)
    except KeyboardInterrupt:
        print("\nExiting...")
    del kc