#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import string


def gen_passwds_file(filename: str, rank_no: int, num_passwds: int):
    if not os.path.exists(filename):
        passwds = gen_passwds_by_rank_no(rank_no, num_passwds)
        with open(filename, "w") as f:
            f.write("\n".join(passwds))


def gen_password(char_list, length: int, num_passwds: int) -> str:
    passwords = set()
    for _ in range(num_passwds):
        pw = []
        for _ in range(length):
            c = random.choice(char_list)
            pw.append(c)
        pw = "".join(pw)
        passwords.add(pw)
    return passwords


def gen_passwds_by_rank_no(rank_no: int, num_passwds: int) -> list:
    character_list = ""
    if rank_no == 0:
        # 0
        character_list = string.ascii_lowercase
        length = 6
    elif rank_no == 1:
        # 25
        character_list = string.digits
        length = 6
    elif rank_no == 2:
        # 50
        character_list = string.digits + string.ascii_lowercase
        length = 8
    elif rank_no == 3:
        # 60
        character_list = string.digits + string.ascii_letters
        length = 8
    elif rank_no == 4:
        # 70
        character_list = string.digits + string.ascii_lowercase
        length = 12
    elif rank_no == 5:
        # 80
        character_list = string.digits + string.ascii_letters
        length = 14
    elif rank_no == 6:
        # 90
        character_list = string.digits + string.ascii_letters + string.punctuation
        length = 14
    else:
        print("Invalid rank_no!")
        return

    passwds = gen_password(
        char_list=character_list, length=length, num_passwds=num_passwds
    )

    return passwds


if __name__ == "__main__":
    rank_no = int(
        input(
            "Please input the security level [0-6]; 0: VERY WEAK, ..., 6: VERY SECURE: "
        )
    )
    num_passwds = int(input("Please input the number of passwords: "))
    gen_passwds_file(f"passwords_{rank_no}.txt", rank_no, num_passwds)
    print("Finished!")
