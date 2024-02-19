from pynput.keyboard import Listener

def on_press(k):
    print(k)

with Listener(on_press=on_press) as lis:
    lis.join()