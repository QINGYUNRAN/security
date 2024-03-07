"""
Author: uceewl4 uceewl4@ucl.ac.uk
Date: 2024-03-07 15:59:44
LastEditors: uceewl4 uceewl4@ucl.ac.uk
LastEditTime: 2024-03-07 15:59:51
FilePath: /security/tmp.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

# 2FA in python
import time
import pyotp

key = (
    pyotp.random_base32()
)  # same key create same password, no one else can get the key
print(key)
# key = "mysuperkey" # can also generate manually
totp = pyotp.TOTP(key)
print(totp.now())  # time base for 30 seconds, after that it will exceeed

time.sleep(30)
print(totp.now)  # 30 seconds later, exceed

input_code = input("Enter your 2FA Code.")
print(totp.verify(input_code))  # verify whether the code is the same with the input one
