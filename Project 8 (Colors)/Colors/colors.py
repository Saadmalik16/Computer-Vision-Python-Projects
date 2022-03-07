import turtle
import colorsys

t = turtle.Turtle()
s = turtle.Screen().bgcolor("black") #set bg color
t.color("white")
t.speed(0.3) # speed
t.width(5) # how much line thick
n = 200
h = 0
for i in range (100): # how many times line move
    t.right(59) #direction in which the line move
    for c in range (1): # for 2 way movement of line and space betweeen the lines
        t.forward(i*2) # spacing and speed for forward movement
        c = colorsys.hsv_to_rgb(h,1,0.7) #last factor indicatee the brightness of colors
        #c = colorsys.rgb_to_hls(h,1,0.8) for one color
        h = h + 1/n
        t.color(c)
turtle.exitonclick()