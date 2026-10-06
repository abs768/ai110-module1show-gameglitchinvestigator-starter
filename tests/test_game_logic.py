from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_numeric_comparisons_for_single_digit_and_larger_values():
    assert check_guess(9, 36)[0] == "Too Low"
    assert check_guess(100, 69)[0] == "Too High"


def test_too_high_guess_subtracts_points_on_even_attempt():
    assert update_score(20, "Too High", 2) == 15


def test_too_high_guess_subtracts_points_on_odd_attempt():
    assert update_score(20, "Too High", 1) == 15
