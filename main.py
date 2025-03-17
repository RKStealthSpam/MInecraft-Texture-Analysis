import pyglet
import random
import time
import os
import ast
import math

window = pyglet.window.Window(height=2048)
window.set_caption('Minecraft Texture Analysis')
label = pyglet.text.Label('Minecraft Texture Analysis',
                          font_name='Verdana',
                          font_size=16,
                          x=window.width//2, y=window.width//2,
                          anchor_x='center', anchor_y='center')

label2 = pyglet.text.Label('TEST', x=1, y=1, z=1, color=(255, 0, 0), height=16)


#image = pyglet.image.load(filename=r'Blocks that I just think are different/oak_planks.png')
#sprite = pyglet.sprite.Sprite(image)
#sprite.scale = (64/16)

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


def rgb_to_hsv(rth_rgb):
    if not isinstance(rth_rgb, tuple) and len(rth_rgb) != 3:
        raise TypeError

    rth_r, rth_g, rth_b, = rth_rgb[0]/255, rth_rgb[1]/255, rth_rgb[2]/255
    rth_max = max(rth_r, rth_g, rth_b)
    rth_min = min(rth_r, rth_g, rth_b)
    rth_c = rth_max - rth_min
    if rth_max == rth_min:
        rth_h = 0
    elif rth_max == rth_r:
        rth_h = (60 * ((rth_g - rth_b) / rth_c) + 360) % 360
    elif rth_max == rth_g:
        rth_h = (60 * ((rth_b - rth_r) / rth_c) + 120) % 360
    else:
        rth_h = (60 * ((rth_r - rth_g) / rth_c) + 240) % 360

    if rth_max == 0:
        rth_s = 0
    else:
        rth_s = (rth_c / rth_max) * 100

    rth_v = rth_max * 100

    return round(rth_h), round(rth_s), round(rth_v)


def hsv_distances(hd_hsv_1, hd_hsv_2):
    hd_hue_delta = math.fabs(hd_hsv_2[0] - hd_hsv_1[0])
    #if hd_hue_delta > 180:
    #    hd_hue_delta = math.fabs(360 - hd_hue_delta)


    hd_sat_delta = math.sqrt((hd_hsv_1[1] - hd_hsv_2[1]) ** 2)

    hd_val_delta = math.sqrt((hd_hsv_1[2] - hd_hsv_2[2]) ** 2)

    return tuple((round(hd_hue_delta), round(hd_sat_delta), round(hd_val_delta)))


def rgb_distance(rd_1, rd_2):
    rd_distance = math.sqrt((rd_1[0] - rd_2[0]) ** 2 + (rd_1[1] - rd_2[1]) ** 2 + (rd_1[2] - rd_2[2]) ** 2)
    return rd_distance


def sort_rgb(sr_profiles, sr_target_rgb, sr_hsv_threshold):
    sr_output = []
    sr_target_hsv = rgb_to_hsv(sr_target_rgb)

    for sr_profile in range(len(sr_profiles)):
        sr_rgb = sr_profiles[sr_profile][1]
        sr_hsv = sr_profiles[sr_profile][2]

        sr_rgb_distance = rgb_distance(sr_target_rgb, sr_rgb)
        sr_hsv_distances = hsv_distances(sr_target_hsv, sr_hsv)

        if sr_hsv_threshold != 0 and math.fabs(sr_hsv_distances[0]/180) > sr_hsv_threshold[0]:
            pass
        elif sr_hsv_threshold != 0 and math.fabs(sr_hsv_distances[1]/100) > sr_hsv_threshold[1]:
            pass
        elif sr_hsv_threshold != 0 and math.fabs(sr_hsv_distances[2]/100) > sr_hsv_threshold[2]:
            pass
        else:
            sr_output.append([sr_profiles[sr_profile][0],
                               sr_profiles[sr_profile][1],
                               sr_profiles[sr_profile][2],
                               round(sr_rgb_distance, 3),
                               sr_hsv_distances])

    sr_sort_by_rgb_distance = sorted(sr_output, key=lambda tup: tup[3])

    return sr_sort_by_rgb_distance


def sort_hsv(sh_profiles, sh_target_rgb, sh_hsv_threshold, sh_hsv_weights):
    sh_output = []
    for sh_profile in range(len(sh_profiles)):
        sh_hsv = sh_profiles[sh_profile][2]
        sh_rgb = sh_profiles[sh_profile][1]
        sh_target_hsv = rgb_to_hsv(sh_target_rgb)
        sh_hsv_distances = hsv_distances(sh_target_hsv, sh_hsv)
        sh_rgb_distance = rgb_distance(sh_target_rgb, sh_rgb)
        print(sh_profiles[sh_profile][0] + '      ' + str(sh_hsv_distances))

        if sh_hsv_threshold != 0 and math.fabs(sh_hsv_distances[0]/360) > sh_hsv_threshold[0]:
            pass
        elif sh_hsv_threshold != 0 and math.fabs(sh_hsv_distances[1]/100) > sh_hsv_threshold[1]:
            pass
        elif sh_hsv_threshold != 0 and math.fabs(sh_hsv_distances[2]/100) > sh_hsv_threshold[2]:
            pass
        else:
            sh_hsv_score = ((sh_hsv_distances[0] / 360 * sh_hsv_weights[0]) +
                            (sh_hsv_distances[1] / 100 * sh_hsv_weights[1]) +
                            (sh_hsv_distances[2] / 100 * sh_hsv_weights[2]) +
                            (sh_rgb_distance * sh_hsv_weights[3] / 441)) / (sum(sh_hsv_weights))

            sh_output.append([sh_profiles[sh_profile][0],
                              sh_profiles[sh_profile][1],
                              sh_profiles[sh_profile][2],
                              round(sh_hsv_score, 3),
                              sh_hsv_distances])

    sh_sort_by_rgb_distance = sorted(sh_output, key=lambda tup: tup[3])
    return sh_sort_by_rgb_distance

def text_data_rewrite():
    global texture_data
    global image

    texture_data = open(r'texture_data.txt', 'w').close()
    texture_data = open(r'texture_data.txt', 'a')
    image_names = os.listdir(r'Blocks that I just think are different')
    for texture in range(len(image_names)):
        color_info = []
        image_name = image_names[texture]
        image = pyglet.image.load(filename=rf'Blocks that I just think are different/{image_name}')
        rgb_data = get_rgb_values(image)
        average_rgb = get_average_rgb(rgb_data)
        average_hsl = rgb_to_hsv(average_rgb)

        color_profile = [image_name, average_rgb, average_hsl]
        texture_data.write(str(color_profile) + '\n')
    texture_data.close()


texture_data = open(r'texture_data.txt', 'r')
text_data = texture_data.readlines()
texture_data.close()

color_profiles = []
for entry in range(len(text_data)):
    color_profiles.append(ast.literal_eval(text_data[entry]))
    #print(color_profiles[entry])

image_name = 'red_concrete.png'
image = pyglet.image.load(filename=rf'Blocks that I just think are different/{image_name}')
image_data = get_rgb_values(image)
image_average = get_average_rgb(image_data)
#sorted_rgb = sort_rgb(color_profiles, (255, 0, 0), (0.5, 0.5, 1))
input_rgb = (0, 0, 0)
sorted_hsv = sort_hsv(color_profiles, input_rgb, (1, 0.2, 1), (0.01, 0.01, 2, 0.005))


for profile in range(len(sorted_hsv)):
    print(f'{sorted_hsv[profile][0]:<40} '
          f'{str(sorted_hsv[profile][1][0]):<4} {str(sorted_hsv[profile][1][1]):<4} {str(sorted_hsv[profile][1][2]):<8}'
          f'{str(sorted_hsv[profile][2][0]):<4} {str(sorted_hsv[profile][2][1]):<4} {str(sorted_hsv[profile][2][2]):<8}'
          f'{str(sorted_hsv[profile][3]):<12}'
          f'{str(sorted_hsv[profile][4][0]):<4} {str(sorted_hsv[profile][4][1]):<4} {str(sorted_hsv[profile][4][2]):<8}')

print(len(sorted_hsv))

def draw_icons(dt):
    global image
    global sorted_hsv

    columns = (len(sorted_hsv) // 32) + 1
    window.width = columns * 256
    for texture_num in range(len(sorted_hsv)):
        column = texture_num // 32
        image_name = sorted_hsv[(column * 32) + (texture_num % 32)][0]
        image = pyglet.image.load(filename=rf'Blocks that I just think are different/{image_name}')
        sprite = pyglet.sprite.Sprite(image)
        sprite.scale = 4
        sprite.position = (column * 256, (texture_num % 32) * 64, 0)
        sprite.draw()
        label = pyglet.text.Label(sorted_hsv[(column * 32) + (texture_num % 32)][0],
                                  x=(column * 256) + 72 ,
                                  y=((texture_num % 32) * 64) + 24,
                                  z=1,
                                  color=sorted_hsv[(column * 32) + (texture_num % 32)][1],
                                  height=16)

        label.draw()

@window.event
def on_draw():
    #window.clear()
    #sprite.position = img_coords
    label2.position = (0, 0, 0)
    #sprite.draw()
    label2.draw()
    if len(pointsList) > 31 and False:
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
    if len(pointsList) > 1 and False:
        for line in range(0, len(pointsList) - 1):
            color = int((line/len(pointsList)) * 255)
            pyglet.shapes.Line(x=pointsList[line][0],
                               y=pointsList[line][1],
                               x2=pointsList[line+1][0],
                               y2=pointsList[line+1][1],
                               thickness=2,
                               color=(0, 0, 255, color//2)).draw()


def image_update(dt):
    #global sprite
    #global img_coords
    #global pointsList
    global oldtime
    #img_coords = (random.randrange(0, window.width - round(sprite.width), 1),
    #              random.randrange(0, window.height - round(sprite.height), 1), 0)
    #pointsList.append(img_coords)
    #if len(pointsList) > 31:
    #    pointsList = pointsList[-32:]

    #label2.text = str(1//(time.time()-oldtime))
    oldtime = time.time()

pyglet.clock.schedule_interval(image_update, 1/30)

window.clear()
pyglet.clock.schedule_interval(draw_icons, 1)

#def rand_width(dt):
#    global window
#    window.width = random.randrange(256, 2048)
#pyglet.clock.schedule_interval(rand_width, 1)

pyglet.app.run()