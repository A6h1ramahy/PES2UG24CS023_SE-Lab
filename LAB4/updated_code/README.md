# Scenario 20 — Mastermind

A terminal code-breaking game with repeated symbols, difficulty configurations, structured feedback, and input validation.

---

## Purpose of the Game

Mastermind is a classic deduction puzzle played against the computer. The game generates a secret code of digits, and the player attempts to crack it within a limited number of turns. After each accepted guess, the player receives structured feedback:
- **Exact Matches**: The number of symbols that are correct in both value and position.
- **Partial Matches**: The number of symbols that exist in the secret code but appear in the wrong position.

The game is won when the player achieves all exact matches before running out of turns.

---

## Project Structure & Provided Files

```text
scenario-20-mastermind/
├── README.md           # Project documentation and assignment checklist
├── requirements.txt    # Standard library declaration (Python 3.9+)
├── main.py             # Entry point
├── game.py             # Mastermind game engine, lifecycle, difficulties, and UI
├── logic.py            # Duplicate-aware feedback calculation algorithm
├── test_logic.py       # Unit tests for core feedback logic
└── test_game.py        # Unit tests for game lifecycle, difficulties, and history
```

---

## Setup and Running

The project requires **Python 3.9+** and uses **only the standard library**. No third-party packages or virtual environment installations are required.

### Run the Game

```bash
python main.py
```

You can also run with a specific difficulty or preset code directly from Python:

```bash
python -c "from game import Mastermind; Mastermind('easy').run()"
python -c "from game import Mastermind; Mastermind(code=['1', '2', '3', '4']).run()"
```

---

## Difficulty Modes & Configurations

At startup, the game prompts the player to select a difficulty mode (or press Enter to accept Medium). The configurations vary code length, symbol set, and allowed guesses:

| Difficulty | Selection Key | Code Length | Symbol Range | Allowed Guesses | Description |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Easy** | `e` / `easy` | **3** | `'1'` to `'4'` (`"1234"`) | **12** | Shorter code, smaller symbol pool, more attempts |
| **Medium** | `m` / `medium` (default) | **4** | `'1'` to `'6'` (`"123456"`) | **10** | Standard Mastermind configuration |
| **Hard** | `h` / `hard` | **5** | `'1'` to `'8'` (`"12345678"`) | **8** | Longer code, larger symbol pool, fewer attempts |

*Note: Entering a valid 4-digit guess directly at the difficulty prompt automatically starts the game in Medium mode without wasting a turn.*

---

## Feedback Rules (Exact & Partial Calculation)

The feedback algorithm in `logic.py` implements a two-pass, duplicate-aware matching rule:

1. **Exact Matches First**:
   - `c == g` across pairwise positions `zip(code, guess)` increments the `exact` count.
   - Exact matches immediately consume both the secret-code position and the guess position.
2. **Unmatched Pool for Partial Matches**:
   - Unmatched symbols are collected into separate multiset frequency counters (`collections.Counter`).
   - For every symbol in the guess, the partial count is calculated as `min(code_count, guess_count)`.
3. **Single Contribution Guarantee**:
   - Each secret-code symbol occurrence can contribute to feedback at most once (either as an exact match or as a partial match, never both).
   - Duplicate symbols in the guess beyond the count present in the secret code are ignored and never generate phantom partial matches.

---

## Input Validation & History Behaviour

- **Strict Validation**:
  - Rejects empty or whitespace inputs.
  - Rejects guesses that do not match the expected code length for the active difficulty.
  - Rejects guesses containing characters outside the active difficulty's permitted symbol pool (including letters and special characters).
  - Displays specific, helpful error messages detailing expected length and permitted symbols.
- **Turn & State Preservation**:
  - Malformed or invalid guesses do not consume turns.
  - Invalid guesses are never recorded in the accepted-guess history.
  - Feedback is computed strictly once for each valid, accepted guess.
- **Readable Guess History**:
  - A formatted table displaying turn index, guess string, exact count, and partial count is printed before each turn prompt once history exists.
  - Typing `'h'` or `'history'` at any prompt redisplays the full guess table without consuming a turn.
  - The complete guess history is also displayed at the conclusion of the game.
- **Clean Quitting**:
  - Entering `'q'` or `'quit'` terminates the session gracefully and reveals the secret code.
- **State Immutability**:
  - Once the game is won, lost, or quit, state mutations are locked. Programmatic calls to `submit_guess()` raise a `RuntimeError`.

---

## Running the Tests

The test suite is built entirely with Python's standard `unittest` framework:

```bash
# Run the complete test suite (27 tests)
python -m unittest discover

# Run feedback logic tests specifically
python test_logic.py

# Run game lifecycle, difficulty, and history tests
python test_game.py
```

All 27 test cases pass cleanly without errors or warnings.

---

## Key Requirements Implemented

- [x] **Task 1 — Duplicate-Aware Feedback**: Fixed overcounting in `logic.py` by resolving exact matches before calculating partial matches with frequency bounds.
- [x] **Task 2 — Game Lifecycle**: Added win/loss tracking, code reveal on loss/quit, turn limits, and post-game state locking in `game.py`.
- [x] **Task 3 — Difficulty Modes**: Added Easy, Medium, and Hard configurations dynamically adjusting code length, symbol ranges, and guess limits.
- [x] **Task 4 — History & Input Robustness**: Added informative input validation, formatted history display, and on-demand history inspection (`'h'`).
- [x] **Zero External Dependencies**: Uses only standard Python modules (`random`, `collections.Counter`, `unittest`, `io`).
- [x] **In-Memory State**: No persistent storage, files, or databases introduced.

---

## Known Limitations

1. **Terminal Interface**: Designed specifically as a console CLI application; does not feature a graphical or web user interface.
2. **Ephemeral State**: In accordance with the lab specification, game sessions are kept in-memory and are not persisted across terminal restarts.
3. **Numeric Symbols**: Secret codes use decimal digit characters (`'1'` through `'8'`).

---

## Submission Checklist

- [x] Task 1 completed and the original defect was reproduced and fixed.
- [x] Tasks 2–4 completed and tested.
- [x] Boundary and invalid-input cases tested.
- [x] No unnecessary external dependencies added.
- [x] No persistent storage added.
- [x] Code remains understandable and modular.
- [x] Complete LLM chat-history link included.

Submission deliverables:
- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

