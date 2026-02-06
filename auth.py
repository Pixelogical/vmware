import pyotp

# create a shared secret (store this securely in DB)
secret = "ICBXZEDMYQVZIG2UQ2NN3Y55RK4NH4LO"
print("Secret:", secret)

# create TOTP object
totp = pyotp.TOTP(secret)

# current OTP code (same as Google Authenticator shows)
print("Current OTP:", totp.now())
