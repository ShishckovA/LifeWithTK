from tkinter import *
from tkinter.filedialog import *
import copy
import time

W = 60
H = 40
C = 20
field = [[0 for i in range(W)] for i in range(H)]

def draw_field():
    global canv
    canv.config(width=W * C, height=H * C)
    canv.delete("all")
    for i in range(W):
        canv.create_line(i * C, 0, i * C, H * C)
    for i in range(H):
        canv.create_line(0, i * C, W * C, i * C)
    for i in range(H):
        for j in range(W):
            if field[i][j]:
                field[i][j] = 0
                create_cell(i, j)
    canv.pack()

def create_cell(i, j):
    if not field[i][j]:
        field[i][j] = canv.create_rectangle(j * C, i * C, (j + 1) * C, (i + 1) * C, fill="green")

def delete_cell(i, j):
    if field[i][j]:
        canv.delete(field[i][j])    
        field[i][j] = 0

def moving(event):
    i = event.y // C
    j = event.x // C 
    if 0 <= j < W and 0 <= i < H:
        if (event.state >> 8) % 2: #left button
            create_cell(i, j)
        elif (event.state >> 10) % 2: #right button
            delete_cell(i, j)

def click(event):
    i = event.y // C
    j = event.x // C 
    if 0 <= j < W and 0 <= i < H:
        if event.num == 1: #left button
            create_cell(i, j)
        elif event.num == 3: #right button
            delete_cell(i, j)

def check_life(i, j):
    num_neib = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if not (0 <= x < H and 0 <= y < W):
                continue
            if cfield[x % H][y % W] and (i, j) != (x, y):
                num_neib += 1
    if not cfield[i][j] and num_neib == 3:
        create_cell(i, j)
    if cfield[i][j] and (num_neib < 2 or num_neib > 3):
        delete_cell(i, j)

def loop():
    global cfield, in_game
    if not in_game:
        return
    
    cfield = copy.deepcopy(field)
    for i in range(H):
        for j in range(W):
            check_life(i, j)
    canv.update()
    root.after(20, loop)
    
def start():
    global in_game
    if in_game:
        return
    in_game = True
    root.title("Life - Game started")
    canv.unbind('<Motion>')
    canv.unbind('<Button>')
    loop()

def stop():
    global in_game
    if not in_game:
        return
    in_game = False
    root.title("Life - Game stopped")
    canv.bind('<Motion>', moving)
    canv.bind('<Button>', click)

def clear():
    for i in range(H):
        for j in range(W):
            delete_cell(i, j)
    canv.update()

def _save():
    file_name = asksaveasfilename(defaultextension='.lfsv',
                                    filetypes=[("Life Save", "*.lfsv"),
                                               ("Все файлы", "*.*")])
    if not file_name:
        return

    out = open(file_name, "w")
    out.write(str(H) + " " + str(W) + "\n")
    for i in range(H):
        for j in range(W):
            if field[i][j]:
                out.write("1 ")
            else:
                out.write("0 ")
        out.write("\n")
    out.close()

def _open():
    global field, W, H
    file_name = askopenfilename(defaultextension='.lfsv',
                                  filetypes=[("Life Save", "*.lfsv"),
                                             ("Все файлы", "*.*")])
    if not file_name:
        return

    try:
        _in = open(file_name, "r")
        cH, cW = map(int, _in.readline().split())
        cfield = [[0 for i in range(cW)] for i in range(cH)]
        for i in range(cH):
            l = _in.readline().split()
            for j in range(cW):
                cfield[i][j] = int(l[j])
        field = cfield
        W, H = cW, cH
        draw_field()
    except BaseException as e:
        print("error loading")
        print(e)

root = Tk()
canv = Canvas(root, width=W * C, height=H * C)
for i in range(W):
    canv.create_line(i * C, 0, i * C, H * C)
for i in range(H):
    canv.create_line(0, i * C, W * C, i * C)

start_b = Button(root, text="Start life", command=start)
stop_b = Button(root, text="Stop life", command=stop)
clear_b = Button(root, text="Clear", command=clear)
save_b = Button(root, text="Save", command=_save)
open_b = Button(root, text="Open", command=_open)


start_b.pack()
stop_b.pack()
clear_b.pack()
save_b.pack()
open_b.pack()

in_game = False
root.title("Life - Game stopped")

canv.bind('<Motion>', moving)
canv.bind('<Button>', click)
canv.pack()

root.mainloop()