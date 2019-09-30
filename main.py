import pygame as pg
import tkinter as tk
from tkinter import filedialog
import random as rd
import sys

scale = 1

white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
deepskyblue = (0, 191, 255, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 100, 255)
lightblue = (0, 0, 255, 255)
steelblue = (70, 130, 180, 255)

coral = (255, 127, 80, 255)
orange = (255, 165, 0, 255)
purple = (230, 0, 230, 255)
pink = (225, 0, 127, 255)
yellow = (230, 230, 0, 255)
gray = (169, 169, 169, 255)
black = (90, 90, 90, 255)


class Node:
    def __init__(self, point=None, back_node=None):
        self.point = point
        self.back_node = back_node

        self.f = 0
        self.h = 0
        self.g = 0

    def __eq__(self, other):
        return self.point[0] == other.point[0] and self.point[1] == other.point[1]


def is_out_of_bound(point):
    return point[0] > 1280 - 1 or point[1] > 720 - 1


def breadth_first(display, start_posi, end_posi, max_x, max_y):
    start = Node(start_posi, None)
    end = Node(end_posi, None)

    frontier = [start]
    to_draw_f = []
    passed_node = []
    to_draw_p = []




def find_path_astar(display, start_posi, end_posi, max_x, max_y):
    start = Node(start_posi, None)
    end = Node(end_posi, None)

    frontier = [start]
    to_draw_f = []
    passed_node = []
    to_draw_p = []

    while len(frontier) > 0:
        curr_node = frontier[0]
        curr_index = 0
        for index, item in enumerate(frontier):
            if item.f < curr_node.f:
                curr_node = item
                curr_index = index

        frontier.pop(curr_index)
        passed_node.append(curr_node)
        to_draw_p.append(curr_node)

        if curr_node == end:
            path = []
            node = curr_node
            while node is not None:
                path.append(node.point)
                node = node.back_node
            for cell in path:
                draw_cell(display, cell, lightblue)
            draw_cell(display, start_pos, blue)
            draw_cell(display, end_pos, red)
            return curr_node.f

        next_nodes = []
        for next in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_node = (curr_node.point[0] + next[0], curr_node.point[1] + next[1])
            cross = False
            if next[0] != 0 and next[1] != 0:
                cross = True

            if new_node[0] > max_x - 1 or new_node[0] < 0 or new_node[1] > max_y - 1 or new_node[1] < 0:
                continue

            if scale != 1 and is_out_of_bound(
                    (new_node[0] * scale + int(scale / 5), new_node[1] * scale + int(scale / 5))):
                continue

            # Xét không đi xéo qua hình
            if cross:
                x_color = pg.Surface.get_at(display, (
                new_node[0] * scale + int(scale / 2), curr_node.point[1] * scale + int(scale / 2)))
                if x_color == purple or p_color == black or p_color == yellow or p_color == pink or p_color == coral or p_color == orange:
                    continue
                y_color = pg.Surface.get_at(display, (
                curr_node.point[0] * scale + int(scale / 2), new_node[1] * scale + int(scale / 2)))
                if y_color == purple or p_color == black or p_color == yellow or p_color == pink or p_color == coral or p_color == orange:
                    continue

            p_color = pg.Surface.get_at(display,
                                        (new_node[0] * scale + int(scale / 2), new_node[1] * scale + int(scale / 2)))
            if p_color == purple or p_color == black or p_color == yellow or p_color == pink:
                continue

            next_node = Node(new_node, curr_node)
            next_nodes.append(next_node)

        for node in next_nodes:
            if node in passed_node:
                continue

            node.g = curr_node.g + 1
            if cross:
                node.g += 0.4
            node.h = (node.point[0] - end.point[0]) ** 2 + (node.point[1] - end.point[1]) ** 2
            node.f = node.g + node.h

            if node in frontier:
                continue

            frontier.append(node)
            to_draw_f.append(node)

        for node in to_draw_p:
            draw_cell(display, node.point, green)
        to_draw_p.clear()

        for node in to_draw_f:
            draw_cell(display, node.point, steelblue)
        to_draw_f.clear()

        pg.display.update()


def flip_y(point):
    return point[0], int(719 / scale) - point[1]


def get_scale(point):
    return point[0] * scale, point[1] * scale


def get_cell(x, y):
    x *= scale
    y *= scale
    return (x + int(scale / 20) + 1, y + int(scale / 20) + 1), (x - int(scale / 20) - 1 + scale, y + int(scale / 20) + 1), (
        x - int(scale / 20) - 1 + scale, y - int(scale / 20) - 1 + scale), (x + int(scale / 20) + 1, y - int(scale / 20) - 1 + scale)


def draw_grid(display):
    if scale == 1:
        return
    for i in range(0, 1280, scale):
        pg.draw.line(display, gray, (i, 0), (i, 720))
    for i in range(0, 720, scale):
        pg.draw.line(display, gray, (0, i), (1280, i))


def draw_cell(display, point, colour):
    if scale == 1:
        pg.draw.circle(display, colour, point, 0)
    else:
        pg.draw.polygon(display, colour, get_cell(point[0], point[1]))


# Vẽ 1 hình từ các đỉnh
def draw_shape(display, points):
    scaled = []
    if scale == 1:
        scaled = points
    else:
        for i in points:
            scaled.append((i[0] * scale + int(scale / 2) + 1, i[1] * scale + int(scale / 2) + 1))

    rd_color = (purple, pink, yellow, black, coral, orange)
    rand = rd_color[rd.randint(0, 5)]
    pg.draw.polygon(display, rand, scaled)

    if scale == 1:
        return

    x_max = 0
    y_max = 0
    x_min = 1000
    y_min = 1000
    for i in scaled:
        if x_max < i[0]:
            x_max = i[0]
        if y_max < i[1]:
            y_max = i[1]
        if x_min > i[0]:
            x_min = i[0]
        if y_min > i[1]:
            y_min = i[1]

    cell_to_draw = []
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            p_color = pg.Surface.get_at(display, (i, j))
            if p_color == rand:
                cell_to_draw.append((int(i / scale), int(j / scale)))
    pg.draw.polygon(display, white, scaled)

    for cell in cell_to_draw:
        draw_cell(display, cell, rand)
    cell_to_draw.clear()

    draw_grid(display)


def open_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    file = open(file_path, 'r')

    size = [int(i) for i in str(file.readline()).split(',')]
    global scale
    scale = min(int(1280 / size[0]), int(720 / size[1]))

    start_end = [int(i) for i in str(file.readline()).split(',')]
    global start_pos
    start_pos = (start_end[0], start_end[1])
    global end_pos
    end_pos = (start_end[2], start_end[3])

    # Bỏ dòng số lượng vì ko cần xài
    file.readline()

    point_set = []
    for line in file:
        point_set.append([int(i) for i in str(line).split(',')])

    polygons = []
    for points in point_set:
        i = 0
        polygon = []
        while i < len(points):
            polygon.append(flip_y((points[i], points[i + 1])))
            i += 2
        polygons.append(polygon)
    global polygon_set
    polygon_set = polygons

    global run_sim
    run_sim = True

    wd.destroy()


def start_sim():
    global start_pos
    start_pos = [int(i) for i in str(e1.get()).split(',')]
    global end_pos
    end_pos = [int(i) for i in str(e2.get()).split(',')]

    size = [int(i) for i in str(e3.get()).split(',')]
    global scale
    scale = min(int(1280 / size[0]), int(720 / size[1]))
    global run_sim
    run_sim = True
    wd.destroy()


def end_prog():
    global run
    run = False
    wd.destroy()


pg.init()

run = True
run_sim = False
start_pos = []
end_pos = []
polygon_set = []
no_input = True

while run:
    wd = tk.Tk()
    wd.title('Project 1 - Path finding')
    wd.attributes("-topmost", True)

    l1 = tk.Label(wd, text="Start Point: ")
    l1.config(font=("Time new Roman", 14))
    l1.grid(row=0, column=0)
    l2 = tk.Label(wd, text="End Point: ")
    l2.config(font=("Time new Roman", 14))
    l2.grid(row=1, column=0)
    l3 = tk.Label(wd, text="Map size: ")
    l3.config(font=("Time new Roman", 14))
    l3.grid(row=2, column=0)

    e1 = tk.Entry(wd)
    e1.config(font=("Time new Roman", 12))
    e1.grid(row=0, column=1)
    e1.insert(0, "10,10")
    e2 = tk.Entry(wd)
    e2.config(font=("Time new Roman", 12))
    e2.grid(row=1, column=1)
    e2.insert(0, "60,30")
    e3 = tk.Entry(wd)
    e3.config(font=("Time new Roman", 12))
    e3.grid(row=2, column=1)
    e3.insert(0, "128, 72")

    b1 = tk.Button(wd, text="Start", width=15, command=start_sim)
    b1.config(font=("Time new Roman", 14))
    b2 = tk.Button(wd, text="Exit", width=15, command=end_prog)
    b2.config(font=("Time new Roman", 14))
    b3 = tk.Button(wd, text="Read from file", width=15, command=open_file)
    b3.config(font=("Time new Roman", 14))
    b1.grid(row=4, column=0)
    b2.grid(row=4, column=1)
    b3.grid(row=3, column=1)

    wd.mainloop()

    if not run_sim:
        sys.exit()

    start_pos = flip_y(start_pos)
    end_pos = flip_y(end_pos)

    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Simulation")
    screen.fill(white)

    for polygon in polygon_set:
        draw_shape(screen, polygon)

    draw_grid(screen)
    if scale != 1:
        draw_cell(screen, start_pos, blue)
        draw_cell(screen, end_pos, red)
    else:
        pg.draw.circle(screen, blue, start_pos, 5)
        pg.draw.circle(screen, red, end_pos, 5)

    pg.display.update()

    print(scale)

    while run_sim:
        pg.time.delay(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run_sim = False
            elif pg.mouse.get_pressed()[0]:
                color = pg.Surface.get_at(screen, pg.mouse.get_pos())
                if color == white and no_input:
                    if scale != 1:
                        draw_cell(screen, (int(pg.mouse.get_pos()[0] / scale), int(pg.mouse.get_pos()[1] / scale)),
                                  black)
                        draw_cell(screen, (int(pg.mouse.get_pos()[0] / scale) + 1, int(pg.mouse.get_pos()[1] / scale)),
                                  black)
                        draw_cell(screen, (int(pg.mouse.get_pos()[0] / scale), int(pg.mouse.get_pos()[1] / scale) + 1),
                                  black)
                        draw_cell(screen, (int(pg.mouse.get_pos()[0] / scale) - 1, int(pg.mouse.get_pos()[1] / scale)),
                                  black)
                        draw_cell(screen, (int(pg.mouse.get_pos()[0] / scale), int(pg.mouse.get_pos()[1] / scale) - 1),
                                  black)
                        draw_cell(screen,
                                  (int(pg.mouse.get_pos()[0] / scale) + 1, int(pg.mouse.get_pos()[1] / scale) - 1),
                                  black)
                        draw_cell(screen,
                                  (int(pg.mouse.get_pos()[0] / scale) + 1, int(pg.mouse.get_pos()[1] / scale) - 1),
                                  black)
                        draw_cell(screen,
                                  (int(pg.mouse.get_pos()[0] / scale) + 1, int(pg.mouse.get_pos()[1] / scale) + 1),
                                  black)
                        draw_cell(screen,
                                  (int(pg.mouse.get_pos()[0] / scale) - 1, int(pg.mouse.get_pos()[1] / scale) + 1),
                                  black)
                    else:
                        pg.draw.circle(screen, black, pg.mouse.get_pos(), 5)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    cost = find_path_astar(screen, start_pos, end_pos, 1280 / scale, 720 / scale)
                    run_sim = False
        pg.display.update()

    mess = tk.Tk()
    mess.title('Completed')
    mess.attributes("-topmost", True)
    l_time = tk.Label(mess, text="Total cost: " + "{0:.3f}".format(cost))
    l_time.config(font=("Time new Roman", 18))
    l_time.pack()

    b_mess = tk.Button(mess, text="Close", command=mess.destroy)
    b_mess.config(font=("Time new Roman", 14))
    b_mess.pack()

    mess.mainloop()

    no_input = True
    pg.quit()
