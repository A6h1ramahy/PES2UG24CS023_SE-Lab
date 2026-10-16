import io
import unittest
from unittest.mock import patch
from game import Mastermind


class TestMastermindGameLifecycle(unittest.TestCase):
    def test_win_immediate(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        res = game.submit_guess("1234")
        self.assertEqual(res, (4, 0))
        self.assertTrue(game.is_won)
        self.assertTrue(game.is_finished)
        self.assertEqual(game.turns, 9)
        self.assertEqual(game.history, [("1234", 4, 0)])

    def test_win_on_final_turn(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=3)
        # 2 wrong guesses
        game.submit_guess("5656")
        game.submit_guess("5656")
        self.assertEqual(game.turns, 1)
        self.assertFalse(game.is_finished)

        # 3rd and final guess correct
        res = game.submit_guess("1234")
        self.assertEqual(res, (4, 0))
        self.assertTrue(game.is_won)
        self.assertTrue(game.is_finished)
        self.assertEqual(game.turns, 0)
        self.assertEqual(len(game.history), 3)

    def test_loss_exhausting_turns(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=3)
        game.submit_guess("5656")
        game.submit_guess("5656")
        res = game.submit_guess("5656")
        self.assertEqual(res, (0, 0))
        self.assertFalse(game.is_won)
        self.assertTrue(game.is_finished)
        self.assertEqual(game.turns, 0)
        self.assertEqual(len(game.history), 3)

    def test_clean_quit(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        game.submit_guess("1111")
        self.assertFalse(game.is_finished)
        game.quit()
        self.assertTrue(game.is_finished)
        self.assertFalse(game.is_won)
        self.assertEqual(game.turns, 9)

    def test_prevent_state_change_after_win(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        game.submit_guess("1234")
        self.assertTrue(game.is_finished)

        with self.assertRaises(RuntimeError):
            game.submit_guess("1234")

        self.assertEqual(game.turns, 9)
        self.assertEqual(len(game.history), 1)

    def test_prevent_state_change_after_loss(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=1)
        game.submit_guess("5656")
        self.assertTrue(game.is_finished)

        with self.assertRaises(RuntimeError):
            game.submit_guess("1234")

        self.assertEqual(game.turns, 0)
        self.assertEqual(len(game.history), 1)

    def test_prevent_state_change_after_quit(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        game.quit()
        self.assertTrue(game.is_finished)

        with self.assertRaises(RuntimeError):
            game.submit_guess("1234")

        self.assertEqual(game.turns, 10)
        self.assertEqual(len(game.history), 0)

    def test_invalid_guess_does_not_consume_turn_or_history(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        self.assertIsNone(game.submit_guess("12"))      # Too short
        self.assertIsNone(game.submit_guess("12345"))   # Too long
        self.assertIsNone(game.submit_guess("1278"))    # Invalid digits
        self.assertIsNone(game.submit_guess("abcd"))    # Letters

        self.assertEqual(game.turns, 10)
        self.assertEqual(len(game.history), 0)
        self.assertFalse(game.is_finished)

    @patch("builtins.input", side_effect=["1234"])
    def test_run_win_output(self, mock_input):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run()
            output = mock_stdout.getvalue()
            self.assertIn("Cracked the code!", output)
            self.assertNotIn("Game Over!", output)

    @patch("builtins.input", side_effect=["5555", "5555"])
    def test_run_loss_output_reveals_code(self, mock_input):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=2)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run()
            output = mock_stdout.getvalue()
            self.assertIn("Game Over! You ran out of turns.", output)
            self.assertIn("1234", output)

    @patch("builtins.input", side_effect=["q"])
    def test_run_quit_output_reveals_code(self, mock_input):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run()
            output = mock_stdout.getvalue()
            self.assertIn("You quit the game.", output)
            self.assertIn("1234", output)


class TestMastermindDifficultyModes(unittest.TestCase):
    def test_difficulty_configurations(self):
        # Easy
        easy_game = Mastermind(difficulty="easy")
        self.assertEqual(easy_game.code_length, 3)
        self.assertEqual(easy_game.symbols, "1234")
        self.assertEqual(easy_game.max_turns, 12)
        self.assertEqual(easy_game.turns, 12)
        self.assertEqual(len(easy_game.code), 3)
        self.assertTrue(all(ch in "1234" for ch in easy_game.code))

        # Medium
        medium_game = Mastermind(difficulty="medium")
        self.assertEqual(medium_game.code_length, 4)
        self.assertEqual(medium_game.symbols, "123456")
        self.assertEqual(medium_game.max_turns, 10)
        self.assertEqual(medium_game.turns, 10)
        self.assertEqual(len(medium_game.code), 4)
        self.assertTrue(all(ch in "123456" for ch in medium_game.code))

        # Hard
        hard_game = Mastermind(difficulty="hard")
        self.assertEqual(hard_game.code_length, 5)
        self.assertEqual(hard_game.symbols, "12345678")
        self.assertEqual(hard_game.max_turns, 8)
        self.assertEqual(hard_game.turns, 8)
        self.assertEqual(len(hard_game.code), 5)
        self.assertTrue(all(ch in "12345678" for ch in hard_game.code))

    def test_easy_mode_validation_and_play(self):
        game = Mastermind(difficulty="easy", code=["1", "2", "3"])
        # In Easy mode: code length must be 3, symbols from "1234"
        self.assertIsNone(game.submit_guess("12"))      # Too short
        self.assertIsNone(game.submit_guess("1234"))    # Too long (valid in medium, but invalid in easy)
        self.assertIsNone(game.submit_guess("125"))     # '5' invalid in easy (only 1-4 allowed)
        self.assertEqual(game.turns, 12)               # No turns consumed

        # Valid guess with feedback
        res = game.submit_guess("321")
        self.assertEqual(res, (1, 2))                   # '2' exact, '3' and '1' partial
        self.assertEqual(game.turns, 11)

    def test_hard_mode_validation_and_play(self):
        game = Mastermind(difficulty="hard", code=["1", "2", "3", "7", "8"])
        # In Hard mode: code length must be 5, symbols from "12345678"
        self.assertIsNone(game.submit_guess("1234"))    # Too short
        self.assertIsNone(game.submit_guess("123456"))  # Too long
        self.assertIsNone(game.submit_guess("12349"))   # '9' invalid
        self.assertEqual(game.turns, 8)

        # Valid guess using symbol '7' and '8'
        res = game.submit_guess("12378")
        self.assertEqual(res, (5, 0))
        self.assertTrue(game.is_won)
        self.assertTrue(game.is_finished)
        self.assertEqual(game.turns, 7)

    @patch("builtins.input", side_effect=["e", "q"])
    def test_interactive_difficulty_selection_easy(self, mock_input):
        game = Mastermind()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run(prompt_difficulty=True)
            output = mock_stdout.getvalue()
            self.assertIn("Mastermind (Easy)", output)
            self.assertIn("enter 3 digits from 1 to 4", output)
            self.assertEqual(game.difficulty, "easy")
            self.assertEqual(game.code_length, 3)
            self.assertEqual(game.symbols, "1234")
            self.assertEqual(game.turns, 12)

    @patch("builtins.input", side_effect=["h", "q"])
    def test_interactive_difficulty_selection_hard(self, mock_input):
        game = Mastermind()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run(prompt_difficulty=True)
            output = mock_stdout.getvalue()
            self.assertIn("Mastermind (Hard)", output)
            self.assertIn("enter 5 digits from 1 to 8", output)
            self.assertEqual(game.difficulty, "hard")
            self.assertEqual(game.code_length, 5)
            self.assertEqual(game.symbols, "12345678")
            self.assertEqual(game.turns, 8)


class TestMastermindHistoryAndValidation(unittest.TestCase):
    def test_validate_guess_messages(self):
        game = Mastermind(difficulty="medium")

        # Empty guess
        valid, msg = game.validate_guess("")
        self.assertFalse(valid)
        self.assertIn("Empty guess", msg)

        # Length mismatch
        valid, msg = game.validate_guess("12")
        self.assertFalse(valid)
        self.assertIn("Invalid length", msg)
        self.assertIn("expected exactly 4 digits, but got 2", msg)

        valid, msg = game.validate_guess("123456")
        self.assertFalse(valid)
        self.assertIn("expected exactly 4 digits, but got 6", msg)

        # Invalid symbols
        valid, msg = game.validate_guess("1278")
        self.assertFalse(valid)
        self.assertIn("Invalid symbol(s)", msg)
        self.assertIn("'7'", msg)
        self.assertIn("'8'", msg)

        valid, msg = game.validate_guess("12ab")
        self.assertFalse(valid)
        self.assertIn("Invalid symbol(s)", msg)
        self.assertIn("'a'", msg)

        # Valid guess
        valid, msg = game.validate_guess("1234")
        self.assertTrue(valid)
        self.assertIsNone(msg)

    def test_format_history(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        self.assertEqual(game.format_history(), "No accepted guesses yet.")

        game.submit_guess("1111")
        game.submit_guess("1243")

        history_str = game.format_history()
        self.assertIn("--- Guess History ---", history_str)
        self.assertIn("Guess", history_str)
        self.assertIn("Exact", history_str)
        self.assertIn("Partial", history_str)
        self.assertIn("1111", history_str)
        self.assertIn("1243", history_str)

    def test_invalid_guesses_not_in_history_and_turns_preserved(self):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        # Attempt invalid guesses
        game.submit_guess("abc")
        game.submit_guess("9999")
        game.submit_guess("")
        game.submit_guess("12345")

        self.assertEqual(game.turns, 10)
        self.assertEqual(len(game.history), 0)

        # Now submit one valid guess
        game.submit_guess("1256")
        self.assertEqual(game.turns, 9)
        self.assertEqual(len(game.history), 1)
        self.assertEqual(game.history[0][0], "1256")

    @patch("builtins.input", side_effect=["5656", "h", "1234"])
    def test_run_displays_history_and_supports_history_command(self, mock_input):
        game = Mastermind(code=["1", "2", "3", "4"], max_turns=10)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            game.run()
            output = mock_stdout.getvalue()
            # History table header and row should appear in output
            self.assertIn("--- Guess History ---", output)
            self.assertIn("5656", output)
            self.assertIn("Cracked the code!", output)


if __name__ == "__main__":
    unittest.main()


