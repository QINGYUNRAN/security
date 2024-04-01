#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import pandas as pd

from brute_force import bruteForceLogin
from gen_passwds import gen_passwds_file

NUM_PASSWDS = 1000

ACCOUNT_FILEPATH = "../../files/account.csv"
ATTACK_TIMES = 3
HOSTNAME = "http://127.0.0.1:5000/pythonlogin"

df = pd.read_csv(ACCOUNT_FILEPATH)
users = df["username"].values
user_passwds = df["password"].values


def main(times: int, rank_no: int, is_dry_run: bool):
    passwds_filename = f"passwords_{rank_no}.txt"
    gen_passwds_file(passwds_filename, rank_no, NUM_PASSWDS)
    matched_times = 0
    with open(passwds_filename, "r") as f:
        passwds = [line.strip() for line in f.readlines()]
    for _ in range(times):
        for _ in range(ATTACK_TIMES):
            passwd = random.choice(passwds)
            if is_dry_run:
                if passwd in user_passwds:
                    matched_times += 1
            else:
                for user in users:
                    users_info = {
                        user: passwd,
                    }
                    if bruteForceLogin(HOSTNAME, users_info):
                        matched_times += 1

    print(
        f"[{matched_times}/{times}] passwords matched if you can only attack {ATTACK_TIMES} times."
    )


if __name__ == "__main__":
    times = int(input("Please input the number of experiments you want to run: "))
    is_dry_run = input("Do you want to do real attack? True or False: ")
    is_dry_run = True if is_dry_run == "True" else False
    rank_no = int(
        input(
            "Please input the security level [0-6]; 0: VERY WEAK, ..., 6: VERY SECURE: "
        )
    )
    main(times, rank_no, is_dry_run)
