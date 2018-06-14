import tkinter as tk
import main


class Gui:
    #TODO add timer
    def __init__(self, gamestate):
        self.root = tk.Tk()
        self.gamestate = gamestate
        self.game = None
        self.entry = None
        self.button = None
        self.time = tk.StringVar()
        self.current_word_vars = []
        self.current_word_labels = []
        self.next_word_labels = []
        self.next_word_vars = []

    def build_gui(self):
        g = self.gamestate

        self.root.title("Typing Test")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)

        self.draw_row(g.current_row, self.current_word_vars, self.current_word_labels, 0)
        self.draw_row(g.next_row, self.next_word_vars, self.next_word_labels, 1)

        self.entry = tk.Entry(self.root)
        self.entry.grid(row=2, columnspan=10)

        self.button = tk.Button(self.root, text="Start timer", command=lambda: self.game.start())
        self.button.grid(row=3, columnspan=5, sticky="e")
        time = tk.Label(self.root, textvariable=self.time)
        self.time.set("60s")
        
        time.grid(row=3, column=5, columnspan=5, sticky="w")

        self.center()

    def highlight(self, i, last_correct):
        """
        Highlights the i'th word in the current row
        :param i: the word to highlight in the current row [0-10)
        :param correct: boolean if the last word typed was correct
        """
        self.current_word_labels[i]["bg"] = "lightblue"
        if i > 0:
            if last_correct:
                self.current_word_labels[i - 1]["bg"] = "lightgreen"
            else:
                self.current_word_labels[i - 1]["bg"] = "salmon"

    def draw_row(self, row, var_list, lab_list, row_num):
        """
        draws the row specified
        :param row: row to draw
        :param var_list: list of textvars to update
        :param lab_list: list of labels to update
        :param row_num: row in which to draw list
        """
        for label in lab_list:
            label.destroy()

        var_list.clear()
        lab_list.clear()

        for i in range(len(row)):
            word_var = tk.StringVar()
            word_lab = tk.Label(self.root, textvariable=word_var, font="Courier", width=11)
            word_var.set(row[i])
            word_lab.grid(row=row_num, column=i)

            var_list += [word_var]
            lab_list += [word_lab]

    def center(self):
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))