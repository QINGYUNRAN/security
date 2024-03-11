import pyotp
import time
import qrcode

key = "ThisSecretLogini"
#totp = pyotp.TOTP(key)
#print(totp.now())

uri = pyotp.totp.TOTP(key).provisioning_uri(name = "yourself", issuer_name="GongSiMingZi")
print(uri)
qrcode.make(uri).save("totp.png")