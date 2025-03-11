import pyglet
import random
import time

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
oldtime = time.time()


def get_rgb_values(grv_image):
    if not isinstance(grv_image, pyglet.image.ImageData):
        raise TypeError

    grv_image_data = grv_image.get_image_data()
    grv_data = grv_image_data.get_data('RGB', 3*grv_image.width)

    grv_rgb_data = []
    for grv_value in range(len(grv_data)//3):
        grv_rgb_data.append((grv_data[(grv_value * 3) + 0],
                             grv_data[(grv_value * 3) + 1],
                             grv_data[(grv_value * 3) + 2]))

    return grv_rgb_data


def get_average_rgb(gar_list):
    gar_r = 0
    gar_g = 0
    gar_b = 0

    for gar_pixel in range(len(gar_list)):
        gar_r += gar_list[gar_pixel][0]
        gar_g += gar_list[gar_pixel][1]
        gar_b += gar_list[gar_pixel][2]

    return (round(gar_r/len(gar_list)),
            round(gar_g/len(gar_list)),
            round(gar_b/len(gar_list)))


@window.event
def on_draw():
    window.clear()
    sprite.position = img_coords
    label2.position = (0, 0, 0)
    sprite.draw()
    label2.draw()
    if len(pointsList) > 31:
        pyglet.shapes.BezierCurve((pointsList[0][0], pointsList[0][1]),
                                  (pointsList[1][0], pointsList[1][1]),
                                  (pointsList[2][0], pointsList[2][1]),
                                  (pointsList[3][0], pointsList[3][1]),
                                  (pointsList[4][0], pointsList[4][1]),
                                  (pointsList[5][0], pointsList[5][1]),
                                  (pointsList[6][0], pointsList[6][1]),
                                  (pointsList[7][0], pointsList[7][1]),
                                  (pointsList[8][0], pointsList[8][1]),
                                  (pointsList[9][0], pointsList[9][1]),
                                  (pointsList[10][0], pointsList[10][1]),
                                  (pointsList[11][0], pointsList[11][1]),
                                  (pointsList[12][0], pointsList[12][1]),
                                  (pointsList[13][0], pointsList[13][1]),
                                  (pointsList[14][0], pointsList[14][1]),
                                  (pointsList[15][0], pointsList[15][1]),
                                  (pointsList[16][0], pointsList[16][1]),
                                  (pointsList[17][0], pointsList[17][1]),
                                  (pointsList[18][0], pointsList[18][1]),
                                  (pointsList[19][0], pointsList[19][1]),
                                  (pointsList[20][0], pointsList[20][1]),
                                  (pointsList[21][0], pointsList[21][1]),
                                  (pointsList[22][0], pointsList[22][1]),
                                  (pointsList[23][0], pointsList[23][1]),
                                  (pointsList[24][0], pointsList[24][1]),
                                  (pointsList[25][0], pointsList[25][1]),
                                  (pointsList[26][0], pointsList[26][1]),
                                  (pointsList[27][0], pointsList[27][1]),
                                  (pointsList[28][0], pointsList[28][1]),
                                  (pointsList[29][0], pointsList[29][1]),
                                  (pointsList[30][0], pointsList[30][1]),
                                  (pointsList[31][0], pointsList[31][1]),
                                  t=1,
                                  segments=1000,
                                  thickness=2).draw()
    if len(pointsList) > 1 and True:
        for line in range(0, len(pointsList) - 1):
            color = int((line/len(pointsList)) * 255)
            pyglet.shapes.Line(x=pointsList[line][0],
                               y=pointsList[line][1],
                               x2=pointsList[line+1][0],
                               y2=pointsList[line+1][1],
                               thickness=2,
                               color=(0, 0, 255, color//2)).draw()


def image_update(dt):
    global sprite
    global img_coords
    global pointsList
    global oldtime
    img_coords = (random.randrange(0, window.width - round(sprite.width), 1),
                  random.randrange(0, window.height - round(sprite.height), 1), 0)
    pointsList.append(img_coords)
    if len(pointsList) > 31:
        pointsList = pointsList[-32:]

    label2.text = str(1//(time.time()-oldtime))
    oldtime = time.time()

pyglet.clock.schedule_interval(image_update, 1/30)

pyglet.app.run()