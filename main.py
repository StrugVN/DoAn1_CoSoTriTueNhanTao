import pygame as pg
import tkinter as tk
import random as rd

scale = 10

white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
orange = (255, 127, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 125, 255)
lightblue = (0, 0, 255, 255)

purple = (255, 0, 255, 255)
pink = (225, 0, 127, 255)
yellow = (255, 255, 0, 255)
gray = (169, 169, 169, 255)
black = (50, 50, 50, 255)


class Node:
    def __init__(self, point=None, back_node=None):
        self.point = point
        self.back_node = back_node

        self.f = 0
        self.h = 0
        self.g = 0

    def __eq__(self, other):
        return self.point[0] == other.point[0] and self.point[1] == other.point[1]


def find_path_astar(display, start_posi, end_posi, max_x, max_y):
    start = Node(start_posi, None)
    end = Node(end_posi, None)

    frontier = [start]
    to_draw = [start]
    passed_node = []

    while len(frontier) > 0:
        curr_node = frontier[0]
        curr_index = 0
        for index, item in enumerate(frontier):
            if item.f < curr_node.f:
                curr_node = item
                curr_index = index

        frontier.pop(curr_index)
        passed_node.append(curr_node)

        if curr_node == end:
            path = []
            node = curr_node
            while node is not None:
                path.append(node.point)
                node = node.back_node
            for cell in path:
                draw_cell(cell, lightblue)
            draw_cell(start_pos, blue)
            draw_cell(end_pos, red)
            return

        next_nodes = []
        for next in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_node = (curr_node.point[0] + next[0], curr_node.point[1] + next[1])
            if new_node[0] > max_x - 1 or new_node[0] < 0 or new_node[1] > max_y - 1 or new_node[1] < 0:
                continue

            p_color = pg.Surface.get_at(display, (new_node[0]*10 + 2, new_node[1]*10 + 2))
            if p_color == purple or p_color == black or p_color == yellow or p_color == pink:
                continue

            next_node = Node(new_node, curr_node)
            next_nodes.append(next_node)

        for node in next_nodes:
            if node in passed_node:
                continue
            # for _node in passed_node:
            #     if node == _node:
            #         continue

            node.g = curr_node.g + 1
            node.h = (node.point[0] - end.point[0])**2 + (node.point[1] - end.point[1])**2
            node.f = node.g + node.h

            if node in frontier:
                continue
            # for _node in frontier:
            #     if node == _node:
            #         continue

            frontier.append(node)
            to_draw.append(node)

        for node in to_draw:
            p_color = pg.Surface.get_at(display, (node.point[0]*10 + 4, node.point[1]*10 + 4))
            if p_color == white:
                draw_cell(node.point, green)
        to_draw.clear()

        pg.display.update()


def get_scale(point):
    return point[0]*10, point[1]*10


def get_cell(x, y):
    x *= scale
    y *= scale
    return (x + 1, y + 1), (x - 1 + scale, y + 1), (x - 1 + scale, y - 1 + scale), (x + 1, y - 1 + scale)


def draw_grid(display):
    for i in range(0, 1280, scale):
        pg.draw.line(display, gray, (i, 0), (i, 720))
    for i in range(0, 720, scale):
        pg.draw.line(display, gray, (0, i), (1280, i))


def draw_cell(point, colour):
    pg.draw.polygon(screen, colour, get_cell(point[0], point[1]))


# Vẽ 1 hình từ các đỉnh
def draw_shape(display, points):
    scaled = []
    for i in points:
        scaled.append((i[0]*10 + 5, i[1]*10 + 5))

    rd_color = (purple, pink, yellow, black)
    rand = rd_color[rd.randint(0, 3)]
    pg.draw.polygon(display, rand, scaled)

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

    for i in range(x_min, x_max+1):
        for j in range(y_min, y_max+1):
            p_color = pg.Surface.get_at(display, (i, j))
            if p_color == rand:
                draw_cell((int(i/10), int(j/10)), rand)

    draw_grid(display)


pg.init()

run = False
start_pos = []
end_pos = []

wd = tk.Tk()
wd.title('Project 1 - Path finding')

l1 = tk.Label(wd, text="Start Point: ")
l1.config(font=("Time new Roman", 14))
l1.grid(row=0, column=0)
l2 = tk.Label(wd, text="End Point: ")
l2.config(font=("Time new Roman", 14))
l2.grid(row=1, column=0)

e1 = tk.Entry(wd)
e1.config(font=("Time new Roman", 12))
e2 = tk.Entry(wd)
e2.config(font=("Time new Roman", 12))
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e1.insert(0, "20,20")
e2.insert(0, "110,50")


def start_sim():
    global start_pos
    start_pos = [int(i) for i in str(e1.get()).split(',')]
    global end_pos
    end_pos = [int(i) for i in str(e2.get()).split(',')]
    global run
    run = True
    wd.destroy()


b1 = tk.Button(wd, text="Start", width=15, command=start_sim)
b1.config(font=("Time new Roman", 14))
b2 = tk.Button(wd, text="Exit", width=15, command=wd.destroy)
b2.config(font=("Time new Roman", 14))
b1.grid(row=2, column=0)
b2.grid(row=2, column=1)

wd.mainloop()

while run:
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Simulation")
    screen.fill(white)

    draw_grid(screen)
    draw_cell(start_pos, blue)
    draw_cell(end_pos, red)

    pg.display.update()

    point_list = []

    while run:
        pg.time.delay(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif pg.mouse.get_pressed()[0]:
                color = pg.Surface.get_at(screen, pg.mouse.get_pos())
                if color == white:
                    # point_list.append((int(pg.mouse.get_pos()[0]/10), int(pg.mouse.get_pos()[1]/10)))
                    draw_cell((int(pg.mouse.get_pos()[0]/10), int(pg.mouse.get_pos()[1]/10)), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) + 1, int(pg.mouse.get_pos()[1] / 10)), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10), int(pg.mouse.get_pos()[1] / 10) + 1), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) - 1, int(pg.mouse.get_pos()[1] / 10)), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10), int(pg.mouse.get_pos()[1] / 10) - 1), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) + 1, int(pg.mouse.get_pos()[1] / 10) - 1), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) + 1, int(pg.mouse.get_pos()[1] / 10) - 1), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) + 1, int(pg.mouse.get_pos()[1] / 10) + 1), black)
                    draw_cell((int(pg.mouse.get_pos()[0] / 10) - 1, int(pg.mouse.get_pos()[1] / 10) + 1), black)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    find_path_astar(screen, start_pos, end_pos, 128, 72)
                # if event.key == pg.K_SPACE:
                #     if len(point_list) > 2:
                #         draw_shape(screen, point_list)
                #         point_list.clear()

        pg.display.update()

    pg.quit()
    wd.mainloop()
