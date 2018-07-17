import state
import user_interface
import time

class Game():
    def __init__(self, gamestate, gui):
        self.gamestate = gamestate
        self.gui = gui
        self.word_counter = 0
        self.started = False
        self.gui.game = self

    def advance_row(self):
        """
        updates gamestate + gui
        """
        g = self.gamestate
        gui = self.gui
        self.word_counter = 0

        g.update_row()
        gui.draw_row(g.current_row, gui.current_word_vars, gui.current_word_labels, 0)
        gui.draw_row(g.next_row, gui.next_word_vars, gui.next_word_labels, 1)

    def get_user_in(self):
        """
        gets current user input
        """
        self.gamestate.user_word = self.gui.entry.get()

    def start(self):
        self.gamestate.update_current_word()
        self.started = True

    def is_correct(self):
        """
        checks if the user's entry is correct
        :return: True if the user's entry is correct
        """
        accuracy = self.gamestate.accuracy()

        if accuracy == 0:
            self.gamestate.correct_words += 1
            return True

        self.gamestate.wrong_chars += accuracy
        return False

    def update_state(self):
        self.word_counter += 1
        if not self.gamestate.current_row:
            self.advance_row()
        self.gamestate.update_current_word()
        self.gamestate.total_chars += len(self.gamestate.current_word)
        self.gui.delete_entry()

    def run_game(self):
        g = self.gamestate
        gui = self.gui
        correct = None

        while True:
            self.get_user_in()
            if not self.started and g.user_word:
                self.start()

            if self.started:
                break

            gui.root.update()
            gui.root.update_idletasks()

        end_time = time.time() + 60

        while time.time() < end_time:
            self.get_user_in()
            gui.highlight(self.word_counter, correct)
            gui.time.set(str(int(end_time - time.time())) + "s")
            gui.disable_button(gui.start_timer)
            if g.user_word and g.user_word[-1] == " ":
                correct = self.is_correct()
                self.update_state()

            gui.root.update()
            gui.root.update_idletasks()

        print(str(g.correct_words) + " words per minute!")
        if g.total_chars:
            print(str((g.total_chars - g.wrong_chars) / g.total_chars)[2:4] + "% accuracy!")


if __name__ == "__main__":
    # source: https://gist.github.com/deekayen/4148741
    file_path = "data/commonwords.txt"
    g = state.GameState(file_path)

    ui = user_interface.Gui(g)
    ui.build_gui()

    game = Game(g, ui)
    game.run_game()
    exit(0)
