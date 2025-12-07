import bcrypt 
import os

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    # Encode the password to bytes, required by bcrypt 
     password_bytes = plain_text_password.encode("utf-8")
    # Generate a salt and hash the password
     salt = bcrypt.gensalt()
     hashed = bcrypt.hashpw(password_bytes, salt)
     return hashed.decode("utf-8")
    
def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
     password_bytes = plain_text_password.encode("utf-8")
     hashed_bytes = hashed_password.encode("utf-8")
     return bcrypt.checkpw(password_bytes, hashed_bytes)

# TEMPORARY TEST CODE - Remove after testing
test_password = "SecurePassword123"
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")
