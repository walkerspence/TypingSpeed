import random


class GameState:
    def __init__(self, file):
        """
        :param file: path to src of words
        :param user_in: user's input (one char at a time)
        """
        self.file = file
        self.words = self.get_words()
        self.current_row = self.get_row()
        self.next_row = self.get_row()
        self.total_chars = 0
        self.wrong_chars = 0
        self.time = 60
        self.correct_words = 0
        self.user_word = ""

    def get_row(self):
        """
        :return: row of 10 words
        """
        indices = random.sample(range(len(self.words)), 10)
        row = [self.words[i] for i in indices]
        return row

    def get_words(self):
        """
        gets words longer than two chars from instance's src file

        :return: puts generate instance's file into an array
        """
        file = open(self.file)
        words = file.read().split('\n')
        file.close()

        return words

    def update_user_word(self, user_in):
        """
        adds new char to user_row
        """
        self.user_word += user_in

    def update_current_word(self):
        """
        sets current word to next word in current row
        """
        self.current_word = self.current_row.pop(0) + " "

    def update_row(self):
        """
        updates current_row and next_row
        """
        self.current_row = self.next_row
        self.next_row = self.get_row()

    def accuracy(self):
        """
        :return: the number of mistyped letters
        """
        wrong = 0
        i = 0

        user_word_len = len(self.user_word) - 1  # removes space at the end
        current_word_len = len(self.current_word) - 1  # removes space at the end

        for i in range(min(user_word_len, current_word_len)):
            if self.user_word[i] != self.current_word[i]:
                wrong += 1

        wrong += max(user_word_len, current_word_len) - i - 1

        return wrong
