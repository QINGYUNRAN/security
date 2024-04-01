#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple

RANKS = [
    (90, "VERY_SECURE", 6),
    (80, "SECURE", 5),
    (70, "VERY_STRONG", 4),
    (60, "STRONG", 3),
    (50, "AVERAGE", 2),
    (25, "WEAK", 1),
    (0, "VERY_WEAK", 0),
]


def rank_password(password: str) -> Tuple[int, str, int]:
    """Return the password's score, rank, and the rank's no."""
    score = 0

    length = len(password)
    if length <= 4:
        score += 5
    elif length <= 7:
        score += 10
    else:
        score += 25
    # print(f"Length: {length}, score now: {score}")

    all_letters = "".join(filter(lambda c: c if c.isalpha() else "", password))
    mix_upper_lower = False
    if len(all_letters) == 0:
        score += 0
    elif all_letters.isupper() or all_letters.islower():
        score += 10
    else:
        mix_upper_lower = True
        score += 20
    # print(f"Letters: '{all_letters}', score now: {score}")

    all_numbers = "".join(filter(lambda c: c if c.isdigit() else "", password))
    if len(all_numbers) == 0:
        score += 0
    elif len(all_numbers) == 1:
        score += 10
    else:
        score += 20
    # print(f"Numbers: '{all_numbers}', score now: {score}")

    others = "".join(
        filter(lambda c: c if not c.isdigit() and not c.isalpha() else "", password)
    )
    if len(others) == 0:
        score += 0
    elif len(others) == 1:
        score += 10
    else:
        score += 25
    # print(f"Others: '{others}', score now: {score}")

    if len(all_numbers) > 0 and len(others) > 0 and mix_upper_lower:
        score += 5
    elif len(all_letters) > 0 and len(all_numbers) > 0 and len(others) > 0:
        score += 3
    elif len(all_letters) > 0 and len(all_numbers) > 0:
        score += 2

    assert score >= 0, f"Invalid password: {password}!"
    for threshold, rank, no in RANKS:
        if score >= threshold:
            return score, rank, no
