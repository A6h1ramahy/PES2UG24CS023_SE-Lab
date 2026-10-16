import unittest
from logic import feedback


class TestMastermindLogic(unittest.TestCase):
    def test_completely_correct_guess(self):
        code = ["1", "2", "3", "4"]
        guess = ["1", "2", "3", "4"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (4, 0))

    def test_no_matches(self):
        code = ["1", "2", "3", "4"]
        guess = ["5", "6", "5", "6"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (0, 0))

    def test_all_matches_in_wrong_positions(self):
        code = ["1", "2", "3", "4"]
        guess = ["4", "3", "2", "1"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (0, 4))

    def test_repeated_symbols_in_guess_bug_fix(self):
        # Code has single '1', guess has four '1's
        code = ["1", "2", "3", "4"]
        guess = ["1", "1", "1", "1"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (1, 0))

        # Code has single '2', guess has two '2's at wrong positions
        code = ["1", "2", "3", "4"]
        guess = ["2", "5", "2", "6"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (0, 1))

    def test_repeated_symbols_in_code(self):
        # Code has two '1's, guess has one '1' at matching position
        code = ["1", "1", "2", "3"]
        guess = ["1", "4", "5", "6"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (1, 0))

        # Code has two '1's, guess has one '1' at non-matching position
        code = ["1", "1", "2", "3"]
        guess = ["4", "5", "1", "6"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (0, 1))

    def test_mixture_of_exact_and_partial_matches(self):
        # Two exact ('1' at index 0, '2' at index 3) and two partial ('2' at 1, '1' at 2)
        code = ["1", "1", "2", "2"]
        guess = ["1", "2", "1", "2"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (2, 2))

        # Two exact ('1's at 0, 1), one partial ('2' at index 3), excess '1' at 2 ignored
        code = ["1", "1", "2", "3"]
        guess = ["1", "1", "1", "2"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (2, 1))

        # One exact ('2' at index 1), one partial ('2' at index 2), excess '2' ignored
        code = ["2", "2", "3", "4"]
        guess = ["1", "2", "2", "2"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (1, 1))

    def test_arbitrary_code_lengths(self):
        # Length 3
        code = ["1", "2", "3"]
        guess = ["1", "3", "2"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (1, 2))

        # Length 5 with letters
        code = ["A", "B", "C", "D", "E"]
        guess = ["A", "C", "B", "E", "D"]
        exact, partial = feedback(code, guess)
        self.assertEqual((exact, partial), (1, 4))


if __name__ == "__main__":
    unittest.main()
