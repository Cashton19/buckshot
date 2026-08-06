import pygame as py

py.init()

screen = py.display.set_mode((1200, 600))

py.display.set_caption("Buckshot")
icon = py.image.load("../assets/game_logo.png")
py.display.set_icon(icon)

# Game loop
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Game logic

