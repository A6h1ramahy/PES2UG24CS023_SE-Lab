from collections import Counter


def feedback(code, guess):
    """
    Compute exact and partial matches for a Mastermind guess against secret code.

    1. Exact matches (correct symbol at correct index) are resolved first and consume
       the corresponding position in both code and guess.
    2. Partial matches (correct symbol at incorrect index) are computed strictly from
       the remaining unmatched symbols, with each secret-code occurrence contributing
       at most once.
    """
    exact = 0
    unmatched_code = []
    unmatched_guess = []

    for c, g in zip(code, guess):
        if c == g:
            exact += 1
        else:
            unmatched_code.append(c)
            unmatched_guess.append(g)

    code_counts = Counter(unmatched_code)
    guess_counts = Counter(unmatched_guess)

    partial = sum(min(code_counts[sym], guess_counts[sym]) for sym in guess_counts)
    return exact, partial

