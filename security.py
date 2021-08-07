#Importing libraries
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

#Get hash from a string
def get_hash(string):
  byte_string = string.encode()
  digest = hashes.Hash(hashes.SHA256() , backend=default_backend()) #Creates a SHA256 hash instance
  digest.update(byte_string) #Data is hashed using the 
  hashed_string = digest.finalize() #Finalize the current context and return the message digest as bytes.

#Creates a key to encrypt and decrypt passwords
def generate_key():
  return Fernet.generate_key()

#Encryption of password
def encrypt_password(key , password):
  f = Fernet(key)
  token = f.encrypt(password.encode())
  return token

#Decryption of password
def decrypt_password(key , encrypted_password):
  f = Fernet(key)
  password = f.decrypt(encrypted_password.encode())
  return password.decode()