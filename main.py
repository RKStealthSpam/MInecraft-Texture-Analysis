import pyglet
import random

window = pyglet.window.Window()
window.set_caption('Minecraft Texture Analysis')
label = pyglet.text.Label('Minecraft Texture Analysis',
                          font_name='Verdana',
                          font_size=16,
                          x=window.width//2, y=window.width//2,
                          anchor_x='center', anchor_y='center')

label2 = pyglet.text.Label('TEST', x=1, y=1, z=1, color=(255, 0, 0), height=16)


image = pyglet.image.load(filename=r'Blocks that I just think are different/oak_planks.png')
sprite = pyglet.sprite.Sprite(image)
sprite.scale = (100/16)

img_coords = (1, 2, 0)
pointsList = [img_coords]
# Define rectangle properties
rect_x = 100
rect_y = 100
rect_width = 50
rect_height = 30
speed_x = 150  # pixels per second
speed_y = 100  # pixels per second
print(label2.height)

@window.event
def on_draw():
    window.clear()
    sprite.position = img_coords
    label2.position = (sprite.position[0], sprite.position[1] - label2.height, sprite.position[2])
    sprite.draw()
    label2.draw()
    if len(pointsList) > 1:
        for line in range(0, len(pointsList) - 1):
            color = int((line/len(pointsList)) * 255)
            pyglet.shapes.Line(x=pointsList[line][0],
                               y=pointsList[line][1],
                               x2=pointsList[line+1][0],
                               y2=pointsList[line+1][1],
                               thickness=2,
                               color=(color, color, color, color)).draw()


def image_update(dt):
    global sprite
    global img_coords
    global pointsList
    img_coords = (random.randrange(0, window.width - round(sprite.width), 1),
                  random.randrange(0, window.height - round(sprite.height), 1), 0)
    pointsList.append(img_coords)
    if len(pointsList) > 64:
        pointsList = pointsList[-64:]
    print(len(pointsList))

pyglet.clock.schedule_interval(image_update, 1/30)

pyglet.app.run()