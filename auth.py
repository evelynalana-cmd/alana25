import bcrypt
import os

def hash_password(plain_text_password):
	# Encode the password to bytes, required by bcrypt
 	password_bytes = plain_text_password.encode('utf-8’)
	# Generate a salt and hash the password
 	salt = bcrypt.gensalt()
 	hashed_password = bcrypt.hashpw(password_bytes, salt)
	# Decode the hash back to a string to store in a text file
	return hashed_ password
	
def verify_password(plain_text_password, hashed_password):
	# Encode both the plaintext password and stored hash to bytes
 	password_bytes = plain_text_password.encode('utf-8’)
 	hashed_password_bytes = hashed_password.encode('utf-8’)
	# bcrypt.checkpw handles extracting the salt and comparing
	return bcrypt.checkpw(password_bytes, hashed_password_bytes)
