#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from rank_passwd import rank_password
from gen_passwds import gen_passwds_file

ACCOUNT_FILEPATH = "../../files/account.csv"
NUM_PASSWDS = 1000


def match_passwd(user_passwds):
    for pw in user_passwds:
        _, _, rank_no = rank_password(pw)
        passwds_filename = f"passwords_{rank_no}.txt"
        gen_passwds_file(passwds_filename, rank_no, NUM_PASSWDS)
        with open(passwds_filename, "r") as f:
            passwds = [line.strip() for line in f.readlines()]
        if pw in passwds:
            return True
    return False


if __name__ == "__main__":
    df = pd.read_csv(ACCOUNT_FILEPATH)
    user_passwds = df["password"].values
    print(f"All user passwords: {user_passwds}")
    matched = match_passwd(user_passwds=user_passwds)
    if matched:
        print("Password matched! Brute-force attack succeed!")
    else:
        print(
            "No matched password. Brute-force attack failed! Please try other passwords!"
        )
