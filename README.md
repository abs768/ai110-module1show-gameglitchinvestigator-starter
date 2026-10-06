# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `pytest`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game purpose

This is a number guessing game built with Streamlit. The game picks a secret
number, and the player has a limited number of attempts to find it. After each
guess the game gives a hint to go higher or lower, and it keeps a score. The
sidebar has three difficulty levels (Easy, Normal and Hard) that set the range
and the number of attempts. The starter version was written by an AI and was full
of bugs, and my job was to find them, fix them and prove the fixes with tests.

### Bugs I found

The full reproduction log, with the input, expected behavior and actual behavior
for each bug, is in [reflection.md](reflection.md).

| # | Bug | Cause in the starter code | Status |
|---|-----|---------------------------|--------|
| 1 | "Attempts left" is one lower than "Attempts allowed" before any guess | `attempts` starts at 1 instead of 0 in `app.py` | Not fixed yet |
| 2 | The hints are backwards (secret 76, guess 2, "Go LOWER!") | The two messages in `check_guess` were swapped | Fixed |
| 3 | The secret is outside the range for the difficulty (Easy is 1 to 20, secret was 36) | The secret is not regenerated when the difficulty changes, and New Game always uses 1 to 100 | Not fixed yet |
| 4 | The same guess gives two different hints, and a wrong guess can earn points | The secret was turned into a string on even attempts, so numbers were compared as text; `update_score` gave +5 for "Too High" on even attempts | Fixed |
| 5 | The debug panel and "Attempts left" are one click behind | They are drawn before the code that handles the guess | Not fixed yet |
| 6 | New Game keeps the old score and history | New Game only resets `attempts` and `secret` | Not fixed yet |

### Fixes I applied

1. **Moved the game logic into `logic_utils.py`.** The four functions
   `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score`
   were inside `app.py`, mixed with the page code. They now live in
   `logic_utils.py` and `app.py` imports them, which lets pytest test them
   without starting Streamlit.
2. **Fixed the reversed hints (bug 2).** In `check_guess`, "Too High" now returns
   "Go LOWER!" and "Too Low" returns "Go HIGHER!". The outcome labels were
   already correct, so only the messages had to be swapped.
3. **Fixed the text comparison (bug 4).** `app.py` no longer converts the secret
   to a string on even attempts, so the guess and the secret are always compared
   as numbers. The `try/except TypeError` fallback in `check_guess` was removed
   because it was the part that compared "9" and "36" as text.
4. **Fixed the score for wrong guesses (bug 4).** `update_score` now takes away
   5 points for every wrong guess. Before, a "Too High" guess on an even attempt
   added 5 points.
5. **Fixed the tests.** The starter tests compared the result of `check_guess` to
   a single string, but the function returns the outcome and the message. I
   updated them and added tests for each fix. An empty `conftest.py` lets pytest
   find `logic_utils.py` from the `tests` folder.

Each fix is marked in the code with a `# FIX:` comment.

## 📸 Demo Walkthrough

A sample game with the fixed code, on Normal difficulty (range 1 to 100). The
secret, shown in the Developer Debug Info panel, was 69.

1. I enter a guess of 9. The game shows "📈 Go HIGHER!" and takes 5 points away.
2. I enter 9 again. The hint is "📈 Go HIGHER!" again. Before the fix, the same
   guess gave a different hint on every second attempt.
3. I enter 9 a third time. The hint is still "📈 Go HIGHER!" and the score is -15.
4. I enter 100. The game shows "📉 Go LOWER!" and the score goes to -20.
5. I enter 69. The game shows "🎉 Correct!" and "You won! The secret was 69.
   Final score: 10", and the game ends.

The score in the debug panel shows up one click late. That is bug 5 in the table
above, which is not fixed yet.

**Screenshot** *(optional)*: not included.

## 🧪 Test Results

```
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.9.0, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/bhavanishankar/AIP1/ai110-module1show-gameglitchinvestigator-starter
collected 6 items

tests/test_game_logic.py ......                                          [100%]

============================== 6 passed in 0.01s ===============================
```

## 🚀 Stretch Features

No stretch features attempted.