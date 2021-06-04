import pygame as pg
import paho.mqtt.client as mqttClient
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
        global Connected  # Use global variable
        Connected = True
    else:
        print("Bad connection Returned code=",rc)

Connected = False
broker_address= "127.0.0.1"
port = 1883

client = mqttClient.Client("Nastya_mqtt")
client.on_connect = on_connect
client.connect(broker_address, port=port)

query = 'drop measurement checkers;'
pg.init()
pg.display.set_caption("C H E C K E R S")
clock = pg.time.Clock()
FPS = 10
W = 700
H = 700
WINDOW_SIZE = (W, H)
BACKGROUND = (150, 90, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (180, 180, 180)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CELL_QTY = 8
CELL_SIZE = 80
R = 30
i = 0
l_free = False
r_free = False
COLORS = [BLACK, GREY]
checkersRed = []
checkersBlue = []
left = []
right = []
screen = pg.display.set_mode(WINDOW_SIZE)
background = pg.Surface(WINDOW_SIZE)
screen.fill(BACKGROUND)
is_even_qty = (CELL_QTY % 2 == 0)
cell_color_index = 1 if (is_even_qty) else 0
list_ch = [0, 0]
ch_number = -1
step = 1

# Create boards
for y in range(CELL_QTY):
    for x in range(CELL_QTY):
        pg.draw.rect(screen, COLORS[cell_color_index], (R + x * CELL_SIZE, R + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        cell_color_index ^= True
    cell_color_index = cell_color_index ^ True if (is_even_qty) else cell_color_index

# Create 12 red checkers
while i < 12:
    for y in range(3):
        if y % 2 == 0:
            for x in range(1, CELL_QTY, 2):
                ch = pg.Rect(30 + CELL_SIZE * x, 30 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                checkersRed.append(ch)
                checker = "checkers,color=red index=%d,X=%d,Y=%d" % (i, ch.centerx, ch.centery)
                #client.loop_start()
                client.publish("checkers", checker)
                #client.loop_stop()
                i += 1
        else:
            for x in range(0, CELL_QTY, 2):
                ch = pg.Rect(30 + CELL_SIZE * x, 30 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                checkersRed.append(ch)
                checker = "checkers,color=red index=%d,X=%d,Y=%d" % (i, ch.centerx, ch.centery)
                # client.loop_start()
                client.publish("checkers", checker)
                # client.loop_stop()
                i += 1

i = 0

# Create 12 blue checkers
while i < 12:
    for y in range(5, CELL_QTY):
        if y % 2 == 0:
            for x in range(1, CELL_QTY, 2):
                ch = pg.Rect(30 + CELL_SIZE * x, 30 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                checker = "checkers,color=blue index=%d,X=%d,Y=%d" % (i, ch.centerx, ch.centery)
                # client.loop_start()
                client.publish("checkers", checker)
                # client.loop_stop()
                checkersBlue.append(ch)
                i += 1
        else:
            for x in range(0, CELL_QTY, 2):
                ch = pg.Rect(30 + CELL_SIZE * x, 30 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                checker = "checkers,color=blue index=%d,X=%d,Y=%d" % (i, ch.centerx, ch.centery)
                # client.loop_start()
                client.publish("checkers", checker)
                # client.loop_stop()
                checkersBlue.append(ch)
                i += 1
# Drawing boards
for y in range(CELL_QTY):
    for x in range(CELL_QTY):
        pg.draw.rect(screen, COLORS[cell_color_index], (R + x * CELL_SIZE, R + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        cell_color_index ^= True
    cell_color_index = cell_color_index ^ True if (is_even_qty) else cell_color_index

pg.image.save(screen, "bg.jpeg")
img = pg.image.load('bg.jpeg')

# New variables
left_free = True
right_free = True
left_fur_free = True
right_fur_free = True
blue_left_check = False
blue_right_check = False
red_left_check = False
red_right_check = False

# main cycle
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    screen.blit(img, (0, 0))
    # drawing 12 red checkers
    for ch in checkersRed:
        pg.draw.circle(screen, RED, (ch.centerx, ch.centery), R)
    # drawing 12 blue checkers
    for ch in checkersBlue:
        pg.draw.circle(screen, BLUE, (ch.centerx, ch.centery), R)

    if step == 1:
        #print("Шаг синих")
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if ch_number != -1:
                for object in list_ch:
                    if object != 0:
                        if object.collidepoint(event.pos):
                            l_free = False
                            r_free = False
                            for ch in checkersRed:
                                if ch.collidepoint((object.centerx + checkersBlue[ch_number].centerx) / 2,
                                                   (object.centery + checkersBlue[ch_number].centery) / 2):
                                    print("\nZASHEL\n")
                                    checkersRed.remove(ch)
                            checker = "checkers,color=blue index=%d,X=%d,Y=%d" % (ch_number, checkersBlue[ch_number].centerx, checkersBlue[ch_number].centery)
                            # client.loop_start()
                            client.publish("checkers", checker)
                            # client.loop_stop()
                            checkersBlue[ch_number].move_ip(object.centerx - checkersBlue[ch_number].centerx,
                                                            object.centery - checkersBlue[ch_number].centery)
                            list_ch = [0, 0]
                            ch_number = -1
                            step = -1
                            break

                for ch in checkersBlue:
                    if ch.collidepoint(event.pos) and step != -1:
                        left = [ch.centerx - 80, ch.centery - 80]
                        right = [ch.centerx + 80, ch.centery - 80]
                        ch_number = checkersBlue.index(ch)
                        left_free = True
                        right_free = True
                        list_ch = [0, 0]
                        for one in checkersBlue:
                            if one.collidepoint(left):
                                blue_left_check = True
                                left_free = False
                            if one.collidepoint(right):
                                blue_right_check = True
                                right_free = False

                        for one in checkersRed:
                            if one.collidepoint(left):
                                left_free = False
                            if one.collidepoint(right):
                                right_free = False
                        if left_free == True:
                            list_ch[0] = pg.Rect(ch.centerx - 120, ch.centery - 120, 80, 80)
                        if right_free == True:
                            list_ch[1] = pg.Rect(ch.centerx + 40, ch.centery - 120, 80, 80)

                        if (left_free == False and blue_left_check == False) or (
                                right_free == False and blue_right_check == False):
                            left_fur_free = True
                            right_fur_free = True
                            left_fur = [left[0] - 80, left[1] - 80]
                            right_fur = [right[0] + 80, right[1] - 80]
                            for one in checkersRed:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            for one in checkersBlue:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            if left_fur_free == True and blue_left_check == False:
                                list_ch[0] = pg.Rect(ch.centerx - 200, ch.centery - 200, 80, 80)
                            if right_fur_free == True and blue_right_check == False:
                                list_ch[1] = pg.Rect(ch.centerx + 120, ch.centery - 200, 80, 80)
                        blue_left_check = False
                        blue_right_check = False

                        # break



            else:
                for ch in checkersBlue:
                    if ch.collidepoint(event.pos) and step != -1:
                        left = [ch.centerx - 80, ch.centery - 80]
                        right = [ch.centerx + 80, ch.centery - 80]
                        ch_number = checkersBlue.index(ch)
                        left_free = True
                        right_free = True
                        list_ch = [0, 0]
                        for one in checkersBlue:
                            if one.collidepoint(left):
                                blue_left_check = True
                                left_free = False
                            if one.collidepoint(right):
                                blue_right_check = True
                                right_free = False

                        for one in checkersRed:
                            if one.collidepoint(left):
                                left_free = False
                            if one.collidepoint(right):
                                right_free = False
                        if left_free == True:
                            list_ch[0] = pg.Rect(ch.centerx - 120, ch.centery - 120, 80, 80)
                        if right_free == True:
                            list_ch[1] = pg.Rect(ch.centerx + 40, ch.centery - 120, 80, 80)

                        if (left_free == False and blue_left_check == False) or (
                                right_free == False and blue_right_check == False):
                            left_fur_free = True
                            right_fur_free = True
                            left_fur = [left[0] - 80, left[1] - 80]
                            right_fur = [right[0] + 80, right[1] - 80]
                            for one in checkersRed:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            if left_fur_free == True and blue_left_check == False:
                                list_ch[0] = pg.Rect(ch.centerx - 200, ch.centery - 200, 80, 80)
                            if right_fur_free == True and blue_right_check == False:
                                list_ch[1] = pg.Rect(ch.centerx + 120, ch.centery - 200, 80, 80)
                        blue_left_check = False
                        blue_right_check = False

                        # break

        if list_ch[0] != 0:
            pg.draw.circle(screen, GREY, (list_ch[0].centerx, list_ch[0].centery), 20)
        if list_ch[1] != 0:
            pg.draw.circle(screen, GREY, (list_ch[1].centerx, list_ch[1].centery), 20)

        if (left_free == True and list_ch[0] != 0) or (left_fur_free == True and list_ch[0] != 0):
            pg.draw.circle(screen, YELLOW, (list_ch[0].centerx, list_ch[0].centery), 10)
        if (right_free == True and list_ch[1] != 0) or (right_fur_free == True and list_ch[1] != 0):
            pg.draw.circle(screen, YELLOW, (list_ch[1].centerx, list_ch[1].centery), 10)

    # if r_free == False and l_free == False:
    # print("No way")

    if step == -1:
        #print("Шаг красных")
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if ch_number != -1:
                for object in list_ch:
                    if object != 0:
                        if object.collidepoint(event.pos):
                            l_free = False
                            r_free = False
                            for ch in checkersBlue:
                                if ch.collidepoint((object.centerx + checkersRed[ch_number].centerx) / 2,
                                                   (object.centery + checkersRed[ch_number].centery) / 2):
                                    print("\nZASHEL\n")
                                    checkersBlue.remove(ch)
                            checker = "checkers,color=red index=%d,X=%d,Y=%d" % (ch_number, checkersBlue[ch_number].centerx, checkersBlue[ch_number].centery)
                            # client.loop_start()
                            client.publish("checkers", checker)
                            # client.loop_stop()
                            checkersRed[ch_number].move_ip(object.centerx - checkersRed[ch_number].centerx,
                                                            object.centery - checkersRed[ch_number].centery)
                            list_ch = [0, 0]
                            ch_number = -1
                            step = 1
                            break

                for ch in checkersRed:
                    if ch.collidepoint(event.pos) and step != 1:
                        left = [ch.centerx - 80, ch.centery + 80]
                        right = [ch.centerx + 80, ch.centery + 80]
                        ch_number = checkersRed.index(ch)
                        left_free = True
                        right_free = True
                        list_ch = [0, 0]
                        for one in checkersRed:
                            if one.collidepoint(left):
                                red_left_check = True
                                left_free = False
                            if one.collidepoint(right):
                                red_right_check = True
                                right_free = False

                        for one in checkersBlue:
                            if one.collidepoint(left):
                                left_free = False
                            if one.collidepoint(right):
                                right_free = False
                        if left_free == True:
                            list_ch[0] = pg.Rect(ch.centerx - 120, ch.centery + 40, 80, 80)
                        if right_free == True:
                            list_ch[1] = pg.Rect(ch.centerx + 40, ch.centery + 40, 80, 80)

                        if (left_free == False and red_left_check == False) or (
                                right_free == False and red_right_check == False):
                            left_fur_free = True
                            right_fur_free = True
                            left_fur = [left[0] - 80, left[1] + 80]
                            right_fur = [right[0] + 80, right[1] + 80]
                            for one in checkersBlue:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            for one in checkersRed:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            if left_fur_free == True and red_left_check == False:
                                list_ch[0] = pg.Rect(ch.centerx - 200, ch.centery + 120, 80, 80)
                            if right_fur_free == True and red_right_check == False:
                                list_ch[1] = pg.Rect(ch.centerx + 120, ch.centery + 120, 80, 80)
                        red_left_check = False
                        red_right_check = False

                        # break



            else:
                for ch in checkersRed:
                    if ch.collidepoint(event.pos) and step != 1:
                        left = [ch.centerx - 80, ch.centery + 80]
                        right = [ch.centerx + 80, ch.centery + 80]
                        ch_number = checkersRed.index(ch)
                        left_free = True
                        right_free = True
                        list_ch = [0, 0]
                        for one in checkersRed:
                            if one.collidepoint(left):
                                red_left_check = True
                                left_free = False
                            if one.collidepoint(right):
                                red_right_check = True
                                right_free = False

                        for one in checkersBlue:
                            if one.collidepoint(left):
                                left_free = False
                            if one.collidepoint(right):
                                right_free = False
                        if left_free == True:
                            list_ch[0] = pg.Rect(ch.centerx - 120, ch.centery + 40, 80, 80)
                        if right_free == True:
                            list_ch[1] = pg.Rect(ch.centerx + 40, ch.centery + 40, 80, 80)

                        if (left_free == False and red_left_check == False) or (
                                right_free == False and red_right_check == False):
                            left_fur_free = True
                            right_fur_free = True
                            left_fur = [left[0] - 80, left[1] + 80]
                            right_fur = [right[0] + 80, right[1] + 80]
                            for one in checkersBlue:
                                if one.collidepoint(left_fur):
                                    left_fur_free = False
                                if one.collidepoint(right_fur):
                                    right_fur_free = False

                            if left_fur_free == True and red_left_check == False:
                                list_ch[0] = pg.Rect(ch.centerx - 200, ch.centery + 120, 80, 80)
                            if right_fur_free == True and red_right_check == False:
                                list_ch[1] = pg.Rect(ch.centerx + 120, ch.centery + 120, 80, 80)
                        red_left_check = False
                        red_right_check = False

                        # break

        if list_ch[0] != 0:
            pg.draw.circle(screen, GREY, (list_ch[0].centerx, list_ch[0].centery), 20)
        if list_ch[1] != 0:
            pg.draw.circle(screen, GREY, (list_ch[1].centerx, list_ch[1].centery), 20)

        if (left_free == True and list_ch[0] != 0) or (left_fur_free == True and list_ch[0] != 0):
            pg.draw.circle(screen, YELLOW, (list_ch[0].centerx, list_ch[0].centery), 10)
        if (right_free == True and list_ch[1] != 0) or (right_fur_free == True and list_ch[1] != 0):
            pg.draw.circle(screen, YELLOW, (list_ch[1].centerx, list_ch[1].centery), 10)

    # if r_free == False and l_free == False:
    # print("No way")

    pg.display.flip()
    clock.tick(FPS)