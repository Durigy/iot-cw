import bcrypt

passwd = 's$cret12'

str_1_encoded = bytes(passwd,'UTF-8')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(str_1_encoded, salt)

if bcrypt.checkpw(str_1_encoded, hashed):
    print("match")
else:
    print("does not match")

# https://zetcode.com/python/bcrypt/
