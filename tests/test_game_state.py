import unittest as test
import state


class TestGenerate(test.TestCase):
    def test_get_words(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)

        words = g.get_words()

        file = open(file_path)
        from_file = file.read()
        file.close()

        self.assertTrue(all((w in from_file) for w in words))
        self.assertTrue(all(len(w) > 2 for w in words))

    def test_get_row(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)
        row = g.get_row()

        self.assertEqual(len(set(row)), len(row)) #check no dupes
        self.assertEqual(10, len(row))

    def test_update_row(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)

        old_next_row = g.next_row
        g.update_row()

        self.assertEqual(old_next_row, g.current_row)

    def test_update_user_row(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)

        self.assertEqual("", g.user_word)

        g.update_user_word("h")

        self.assertEqual("h", g.user_word)

        g.update_user_word("e")
        g.update_user_word("l")
        g.update_user_word("l")
        g.update_user_word("o")

        self.assertEqual("hello", g.user_word)

    def test_update_current_word(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)

        next_word = g.current_row[0] + " "
        next_next_word = g.current_row[1] + " "
        g.update_current_word()
        self.assertEqual(next_word, g.current_word)

        g.update_current_word()
        self.assertEqual(next_next_word, g.current_word)

    def test_accuracy(self):
        file_path = "../data/commonwords.txt"
        g = state.GameState(file_path)
        g.current_word = "malnutrition "  # 12

        g.user_word = "malnutrition "
        self.assertEqual(0, g.accuracy())

        g.user_word = "maln "
        self.assertEqual(8, g.accuracy())

        g.user_word = "manutrition "
        self.assertEqual(10, g.accuracy())

        g.user_word = "malnutritiob "
        self.assertEqual(1, g.accuracy())

        g.user_word = "malnutritio "
        self.assertEqual(1, g.accuracy())

        g.user_word = "malnutritional "
        self.assertEqual(2, g.accuracy())
