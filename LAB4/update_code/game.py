import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "easy": {
            "name": "Easy",
            "code_length": 3,
            "symbols": "1234",
            "symbol_display": "1 to 4",
            "max_turns": 12,
            "description": "3 digits, symbols 1 to 4, 12 turns",
        },
        "medium": {
            "name": "Medium",
            "code_length": 4,
            "symbols": "123456",
            "symbol_display": "1 to 6",
            "max_turns": 10,
            "description": "4 digits, symbols 1 to 6, 10 turns",
        },
        "hard": {
            "name": "Hard",
            "code_length": 5,
            "symbols": "12345678",
            "symbol_display": "1 to 8",
            "max_turns": 8,
            "description": "5 digits, symbols 1 to 8, 8 turns",
        },
    }

    def __init__(self, difficulty=None, code=None, max_turns=None, code_length=None, symbols=None):
        self._custom_code = code is not None
        self._needs_difficulty_prompt = difficulty is None and code is None

        diff_key = difficulty.lower() if isinstance(difficulty, str) else "medium"
        cfg = self.DIFFICULTIES.get(diff_key, self.DIFFICULTIES["medium"])

        self.difficulty = diff_key if diff_key in self.DIFFICULTIES else "medium"
        self.code_length = code_length if code_length is not None else (len(code) if code is not None else cfg["code_length"])
        self.symbols = symbols if symbols is not None else cfg["symbols"]
        self.symbol_display = cfg.get("symbol_display", f"{self.symbols[0]} to {self.symbols[-1]}")
        self.max_turns = max_turns if max_turns is not None else cfg["max_turns"]
        self.turns = self.max_turns

        if code is not None:
            self.code = list(code)
        else:
            self.code = [random.choice(self.symbols) for _ in range(self.code_length)]

        self.history = []
        self.is_finished = False
        self.is_won = False

    def set_difficulty(self, difficulty_key):
        """Update configuration based on chosen difficulty."""
        key = str(difficulty_key).lower().strip()
        if key in ("e", "easy", "1"):
            key = "easy"
        elif key in ("h", "hard", "3"):
            key = "hard"
        else:
            key = "medium"

        cfg = self.DIFFICULTIES[key]
        self.difficulty = key
        self.code_length = cfg["code_length"]
        self.symbols = cfg["symbols"]
        self.symbol_display = cfg["symbol_display"]
        self.max_turns = cfg["max_turns"]
        self.turns = self.max_turns
        if not self._custom_code:
            self.code = [random.choice(self.symbols) for _ in range(self.code_length)]
        self._needs_difficulty_prompt = False

    def validate_guess(self, raw):
        """
        Validate a guess against current difficulty settings.
        Returns (True, None) if valid.
        Returns (False, error_message) if invalid.
        """
        raw = raw.strip() if isinstance(raw, str) else ""
        if not raw:
            return False, f"Empty guess: enter exactly {self.code_length} digits from {self.symbol_display}."

        if len(raw) != self.code_length:
            return False, f"Invalid length: expected exactly {self.code_length} digits, but got {len(raw)}."

        invalid_chars = sorted(set(ch for ch in raw if ch not in self.symbols))
        if invalid_chars:
            chars_str = ", ".join(f"'{ch}'" for ch in invalid_chars)
            return False, f"Invalid symbol(s) {chars_str}: only digits from {self.symbol_display} are permitted."

        return True, None

    def format_history(self):
        """Return a formatted string representing accepted guess history."""
        if not self.history:
            return "No accepted guesses yet."

        col_width = max(self.code_length, 5)
        lines = [
            "\n--- Guess History ---",
            f"  {'#':<4} | {'Guess':<{col_width}} | {'Exact':<5} | {'Partial':<7}",
            f"  {'-'*4}-+-{'-'*col_width}-+-{'-'*5}-+-{'-'*7}",
        ]
        for idx, (guess_str, exact, partial) in enumerate(self.history, start=1):
            lines.append(f"  {idx:<4} | {guess_str:<{col_width}} | {exact:<5} | {partial:<7}")
        lines.append("---------------------\n")
        return "\n".join(lines)

    def display_history(self):
        """Print the readable history of accepted guesses."""
        print(self.format_history())

    def submit_guess(self, raw):
        """
        Submit a guess and update game state.
        Raises RuntimeError if the game has already ended.
        Returns (exact, partial) on valid guess, or None if the guess is invalid.
        """
        if self.is_finished:
            raise RuntimeError("Cannot make a guess: game has already ended.")

        is_valid, _ = self.validate_guess(raw)
        if not is_valid:
            return None

        raw = raw.strip()
        guess = list(raw)
        exact, partial = feedback(self.code, guess)
        self.history.append((raw, exact, partial))
        self.turns -= 1

        if exact == self.code_length:
            self.is_won = True
            self.is_finished = True
        elif self.turns <= 0:
            self.is_finished = True

        return exact, partial

    def quit(self):
        """Cleanly mark the game as finished upon quitting."""
        if self.is_finished:
            return
        self.is_finished = True

    def run(self, prompt_difficulty=True):
        if self.is_finished:
            print("Game has already ended.")
            return

        pending_first_guess = None

        if prompt_difficulty and self._needs_difficulty_prompt:
            print("Select difficulty:")
            for key, cfg in self.DIFFICULTIES.items():
                print(f"  [{key[0].upper()}]{key[1:]}: {cfg['description']}")
            choice = input("Choose difficulty [E/M/H] (Press Enter for Medium): ").strip().lower()
            if choice in ("q", "quit"):
                self.quit()
                print(f"You quit the game. The secret code was {''.join(self.code)}")
                return

            if len(choice) == 4 and all(ch in "123456" for ch in choice):
                self.set_difficulty("medium")
                pending_first_guess = choice
            else:
                self.set_difficulty(choice)

        print(f"Mastermind ({self.difficulty.capitalize()}) - enter {self.code_length} digits from {self.symbol_display}. (Enter 'q' to quit, 'h' for history)")
        while not self.is_finished and self.turns > 0:
            if pending_first_guess is not None:
                raw = pending_first_guess
                pending_first_guess = None
            else:
                if self.history:
                    self.display_history()
                raw = input(f"{self.turns} turns left > ").strip()

            if raw.lower() in ("q", "quit"):
                self.quit()
                print(f"You quit the game. The secret code was {''.join(self.code)}")
                return

            if raw.lower() in ("h", "history"):
                self.display_history()
                continue

            is_valid, err_msg = self.validate_guess(raw)
            if not is_valid:
                print(err_msg)
                continue

            exact, partial = self.submit_guess(raw)
            print(f"Exact: {exact}  Partial: {partial}")

            if self.is_won:
                self.display_history()
                print(f"Cracked the code! Congratulations, you won in {self.max_turns - self.turns} turn(s)!")
                return

        if not self.is_won and self.is_finished:
            self.display_history()
            print("Game Over! You ran out of turns.")
            print("The code was", "".join(self.code))
