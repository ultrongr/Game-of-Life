import tkinter as tk
import numpy as np
import time
import pyautogui as pg

pg.PAUSE = 0


class Win:
    def __init__(self, root):
        self.root = root
        self.simulation = False
        self.paused = False
        self.Table = None
        self.Temp = None
        (self.radius, self.time_step, self.size, self.steps) = (1, 1, 25, 0)
        (self.rows, self.columns, self.stay_alive, self.come_alive, self.starting_time) = (0, 0, 0, 0, 0)
        self.Selections = tk.Canvas(root, width=200, height=800, bg="white")
        self.Selections.grid(row=0, column=0)
        self.Board = tk.Canvas(root, width=1570, height=980, bg="blue")
        self.Board.grid(row=0, column=1, rowspan=20)

        self.pad = tk.Canvas(self.Selections, width=350, height=200, bg="black")
        self.pad.grid(row=0, column=0, columnspan=2)

        self.label0 = tk.Label(self.Selections, text="Size of cells:", bg="white")
        self.label0.grid(row=1, column=0)
        self.esize = tk.Entry(self.Selections)
        self.esize.insert(0, '25')
        self.esize.grid(row=1, column=1)

        self.label1 = tk.Label(self.Selections, text="Number of rows:", bg="white")
        self.label1.grid(row=2, column=0)
        self.label2 = tk.Label(self.Selections, text="Number of columns: ", bg="white")
        self.label2.grid(row=3, column=0)
        self.erows = tk.Entry(self.Selections)
        self.erows.insert(0, '25')
        self.erows.grid(row=2, column=1)
        self.ecolumns = tk.Entry(self.Selections)
        self.ecolumns.insert(0, '25')
        self.ecolumns.grid(row=3, column=1)

        self.label3 = tk.Label(self.Selections, text="Radius of effect:", bg="white")
        self.label3.grid(row=4, column=0)
        self.eradius = tk.Entry(self.Selections)
        self.eradius.insert(0, '1')
        self.eradius.grid(row=4, column=1)

        self.label3 = tk.Label(self.Selections, text="Live cells survive if neighboors:", bg="white")
        self.label3.grid(row=5, column=0)
        self.estay_alive = tk.Entry(self.Selections)
        self.estay_alive.insert(0, '2,3')
        self.estay_alive.grid(row=5, column=1)
        self.label4 = tk.Label(self.Selections, text="Dead cells come alive if neighboors:", bg="white")
        self.label4.grid(row=6, column=0)
        self.ecome_alive = tk.Entry(self.Selections)
        self.ecome_alive.insert(0, '3')
        self.ecome_alive.grid(row=6, column=1)
        self.label5 = tk.Label(self.Selections, text="Time step: ", bg="white")
        self.label5.grid(row=7, column=0)
        self.etime_step = tk.Entry(self.Selections)
        self.etime_step.insert(0, '1')
        self.etime_step.grid(row=7, column=1)

        self.label6 = tk.Label(self.Selections, text="Insert file name of the layout", bg="white")
        self.label6.grid(row=8, column=0)
        self.eload = tk.Entry(self.Selections)
        self.eload.insert(0, '.txt')
        self.eload.grid(row=8, column=1)

        self.create_button = tk.Button(self.Selections, width=15, height=3, command=self.create_board,
                                       text="Create Board")
        self.create_button.grid(row=16, column=0)
        self.start_button = tk.Button(self.Selections, width=15, height=3, command=self.start_simulation,
                                      text="START", state="disabled")
        self.start_button.grid(row=17, column=0)
        self.next_step_button = tk.Button(self.Selections, width=15, height=3, command=self.next_step,
                                          text="NEXT STEP", state="disabled")
        self.next_step_button.grid(row=18, column=0)
        self.end_button = tk.Button(self.Selections, width=15, height=3, command=self.end_simulation,
                                    text="END", state="disabled")
        self.end_button.grid(row=19, column=0)
        self.automate = tk.Button(self.Selections, width=15, height=3, command=self.automate_simulation,
                                  text="AUTOMATE", state="disabled")
        self.automate.grid(row=17, column=1)

        self.load_button = tk.Button(self.Selections, width=15, height=3, command=self.load_layout,
                                     text="LOAD LAYOUT", state="normal")
        self.load_button.grid(row=16, column=1)
        self.save_button = tk.Button(self.Selections, width=15, height=3, command=self.save_layout,
                                     text="SAVE LAYOUT", state="disabled")
        self.save_button.grid(row=18, column=1)

        self.steps_label = tk.Label(self.Selections, text="Steps= " + str(self.steps), bg="yellow", font=("", 32))
        self.steps_label.grid(row=21, column=0, columnspan=2)

    def create_board(self):
        if self.simulation:
            return
        self.steps = 0
        del self.Table
        self.size = int(self.esize.get())
        self.Board.delete("all")
        self.save_button.configure(state="normal")
        self.rows = int(self.erows.get())
        self.columns = int(self.ecolumns.get())
        self.Table = Table(self.Board, self.rows, self.columns, self.size)
        self.Board.bind("<Button-1>", self.cell_click)
        self.start_button.configure(state="normal")

    def cell_click(self, event):
        row = event.y // self.size
        column = event.x // self.size
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.Table.table[row, column].change()

    def start_simulation(self):
        if self.simulation:
            return
        try:
            self.save_button.configure(state="disabled")
            self.load_button.configure(state="disabled")

            self.radius = int(self.eradius.get())
            self.stay_alive = self.estay_alive.get().split(",")
            self.come_alive = self.ecome_alive.get().split(",")
        except:
            print("Something is worng with the ranges!")
            return
        print("Simulation has started")
        self.steps = 0
        self.steps_label.configure(text="Steps= " + str(self.steps))
        self.end_button.configure(state="active")
        self.next_step_button.configure(state="active")
        self.create_button.configure(state="disabled")
        self.automate.configure(state="normal")
        self.Board.unbind("<Button-1>")
        self.simulation = True

    def automate_simulation(self):
        try:
            self.time_step = int(self.etime_step.get())
        except:
            if "." in self.etime_step.get():
                t = self.etime_step.get().split(".")
                self.time_step = int(t[0]) + int(t[1]) * (10 ** (-len(t[1])))
        if not self.simulation or self.paused:
            return
        self.pad.configure(bg="Green")
        self.pad.bind('<Enter>', self.enter)
        self.pad.bind('<Leave>', self.exit)
        self.pad.bind("<Button-1>", self.pad_click)

    def enter(self, event):
        self.entered = True
        pg.click()

    def exit(self, event):
        self.entered = False

    def pad_click(self, event):
        time.sleep(self.time_step)
        if self.entered:
            self.next_step()
            pg.click()

    def end_simulation(self):
        self.simulation = False
        self.paused = False
        self.load_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.create_button.configure(state="normal")
        self.end_button.configure(state="disabled")
        self.next_step_button.configure(state="disabled")
        self.automate.configure(state="disabled")
        self.pad.configure(bg="Black")
        self.pad.unbind('<Enter>')
        self.pad.unbind('<Exit>')
        self.pad.unbind("<Button-1>")

    def next_step(self):
        if not self.simulation or self.paused:
            return
        self.Temp = np.empty([self.rows, self.columns])
        for x in range(self.rows):
            for y in range(self.columns):
                self.Temp[x, y] = self.Table.table[x, y].status

        for x in range(self.rows):
            for y in range(self.columns):
                self.Temp[x, y] = self.Table.table[x, y].status
                blacks_count = 0
                for x1 in range(x - self.radius, x + self.radius + 1):
                    for y1 in range(y - self.radius, y + self.radius + 1):
                        if (x1, y1) != (x, y) and 0 <= x1 < self.rows and 0 <= y1 < self.columns:
                            blacks_count += self.Table.table[x1, y1].status

                if self.Temp[x, y] == 1:
                    if str(blacks_count) not in self.stay_alive:
                        self.Temp[x, y] = 0
                if self.Temp[x, y] == 0:
                    if str(blacks_count) in self.come_alive:
                        self.Temp[x, y] = 1
        for x in range(self.rows):
            for y in range(self.columns):
                if self.Table.table[x][y].status != self.Temp[x][y]:
                    self.Table.table[x][y].change()
        self.steps += 1
        self.steps_label.configure(text="Steps= " + str(self.steps))

    def load_layout(self):
        try:
            counter = 0
            file_name = self.eload.get()
            file = open(file_name, "r", encoding="utf-8-sig")
            for line in file:
                if counter == 0:
                    self.erows.delete(0, 'end')
                    self.ecolumns.delete(0, 'end')
                    self.esize.delete(0, 'end')
                    self.erows.insert(0, line.split("*")[0])
                    self.ecolumns.insert(0, line.split("*")[1])
                    self.esize.insert(0, line.split("*")[2])
                    self.create_board()
                else:
                    x = int(line.split(",")[0])
                    y = int(line.split(",")[1])
                    self.Table.table[x, y].activate()
                counter += 1
        except:
            print("something is wrong with the file!")

    def save_layout(self):
        try:
            file_name = self.eload.get()
            file = open(file_name, "w")

            file.write(self.erows.get() + "*" + self.ecolumns.get() + "*" + str(self.size) + "\n")
            for x in range(0, self.rows):
                for y in range(0, self.columns):
                    if self.Table.table[x][y].status:
                        file.write(str(x) + "," + str(y) + "\n")
            file.close()

        except:
            print("something is wrong with the file!")


class Cell:
    def __init__(self, canvas, row, column, size):
        self.Canvas = canvas
        self.row = row
        self.column = column
        self.status = 0
        self.rect = self.Canvas.create_rectangle(size * column, size * row, size * (column + 1), size * (row + 1),
                                                 fill="white", outline="yellow")

    def activate(self):
        self.status = 1
        self.Canvas.itemconfig(self.rect, fill="black")

    def deactivate(self):
        self.status = 0
        self.Canvas.itemconfig(self.rect, fill="white")

    def change(self):
        self.status = 1 - self.status
        self.Canvas.itemconfig(self.rect, fill=self.status * "black" + (1 - self.status) * "white")


class Table:
    def __init__(self, Canvas, rows, columns, size):
        self.Canvas = Canvas
        self.rows = rows
        self.columns = columns
        self.size = size
        self.table = np.empty([self.rows, self.columns], dtype=Cell)
        self.fill_table()

    def fill_table(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.table[x, y] = Cell(self.Canvas, x, y, self.size)

    def print_table(self):
        for x in range(self.rows):
            for y in range(self.columns):
                print(self.table[x, y].status, end="   ")
            print("\n")


root = tk.Tk()
root.geometry("1900x980+10+10")
root.configure(bg="#96DFCE")
w = Win(root)

root.mainloop()
