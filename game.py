from window import WINDOW

bird=WINDOW("Bird")
while True:
    bird.display()
    x,y=bird.get_position()
    x+=1 
    bird.move_to(x,y)