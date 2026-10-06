# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**What did the game look like the first time you ran it?**

The first time I ran the game, it looked like a simple number guessing game with a
difficulty setting in the sidebar, but the numbers on the screen did not add up.
On Easy the sidebar said "Attempts allowed: 6", but the banner already showed
"Attempts left: 5" before I had made a single guess. On Normal it was the same:
8 attempts allowed, but only 7 left at the start. My guesses also seemed to
register late, because the debug panel was always one guess behind.

**Concrete bugs I noticed at the start**

- The attempts counter was off by one. I lost an attempt before guessing anything.
- The hints were backwards. With a secret of 76 I guessed 2 and it said "Go LOWER!".
- The secret did not match the difficulty. On Easy (range 1 to 20) the secret was 36.
- The same guess gave two different hints. I guessed 9 twice against 36 and got
  "Go HIGHER!" and then "Go LOWER!".
- The debug panel and "Attempts left" were one click behind my actual guesses.
- New Game did not reset the score or the history.

**Game trace (starter code, before any fixes)**

```
Session A - Normal (range 1-100, 8 attempts allowed)
  Banner before guessing: "Attempts left: 7"
  Guesses: 13, 11, 7, 7, 5, 4, 2    Secret: 76
  Guess 2 -> "Go LOWER!"
  -> "Out of attempts! The secret was 76. Score: -35"   (after 7 guesses, not 8)
  History panel still showed 13, 11, 7, 7, 5, 4 (my last guess, 2, was missing)

Session B - Hard (range 1-50, 5 attempts allowed)
  Secret: 12   Guess 11 -> "Go LOWER!"

Session C - Easy, after refreshing the page (Range 1 to 20, Attempts allowed: 6)
  Banner: "Guess a number between 1 and 100. Attempts left: 5"   Secret: 36
  Guess 9 -> "Go HIGHER!"
  Guess 9 -> "Go LOWER!"   Debug panel: Score 5, History [9]

Session D - Normal, clicked New Game after winning
  Before: Score 70, History [11]
  After:  Secret 60, Attempts 0, "Attempts left: 8", Score 70, History [11]
```

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Opened the game on Easy and made no guess | "Attempts left: 6", because 6 attempts are allowed | "Attempts left: 5". On Normal I only got 7 guesses instead of 8 | None |
| Normal, secret 76, guessed 2. Hard, secret 12, guessed 11 | The hint should tell me to go higher, because my guess is below the secret | "Go LOWER!" both times | None |
| Selected Easy (range 1 to 20) and refreshed the page | A secret between 1 and 20, and a banner that says "between 1 and 20" | The secret was 36 (and 25 in another game). The banner said "between 1 and 100" | None |
| Easy, secret 36, guessed 9 two times in a row | The same hint both times, and no points for a wrong guess | First "Go HIGHER!" and my score went up by 5, then "Go LOWER!" | None |
| Submitted a guess and checked the debug panel | History and attempts should update right away | The panel was one guess behind. I entered 4 and it was not in the history until my next click | None |
| Won a game and clicked New Game | Score back to 0 and an empty history | Score stayed at 70 and the history still showed [11]. Only the attempts and the secret changed | None |

**What is causing each bug (line numbers from the starter `app.py`)**

1. **Attempts start at 1 instead of 0.** Line 96 sets `st.session_state.attempts = 1`,
   so one attempt is already used before I guess.
2. **The hints are backwards.** In `check_guess` (lines 37-40) the messages are
   swapped: when the guess is greater than the secret it says "Go HIGHER!", and
   otherwise it says "Go LOWER!".
3. **The secret does not follow the difficulty.** The secret is only created once
   (lines 92-93), so changing the difficulty keeps the old one. New Game always uses
   `random.randint(1, 100)` (line 136), and the banner has "1 and 100" hardcoded
   (line 110).
4. **Numbers are compared as text on every second guess.** At first I thought the
   game was comparing ASCII values, because secret 58 with guess 57 told me to go
   lower. That was not quite right. Lines 158-161 turn the secret into a string on
   even attempts, so Python compares the digits as text, and "9" comes after "36".
   That is why the same guess of 9 gave me two different hints. `update_score`
   (lines 57-60) also gives +5 for a "Too High" result on an even attempt.
5. **The display is one step behind.** The banner and the debug panel (lines
   109-119) are drawn before the code that handles my guess (line 147 onward).
6. **New Game does not reset everything.** Lines 134-138 only reset `attempts` and
   `secret`. The score, history and status are left as they were.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
