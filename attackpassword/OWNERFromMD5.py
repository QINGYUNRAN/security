import hashlib
TapoEmailVictim=b"uceewl4@ucl.ac.uk"
OWNER = hashlib.md5(TapoEmailVictim).hexdigest().upper()
print(OWNER)





