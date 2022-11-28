import base64
import hashlib
from api import NUMBER_OF_HASH_ITERATIONS

def hash_mp_additionally(password_hash: str, salt: str) -> str:
    """Provides additional server side hashing of master password"""
    
    #----------------convert recived password hash and salt to bytes-----------------------
    converted_to_bytes_password_hash = password_hash.encode("utf-8")
    converted_to_bytes_salt = salt.encode("utf-8")

    #----------------additionally hash password 40000 times with salt-----------------------
    additionaly_hashed_master_password = hashlib.pbkdf2_hmac(hash_name="sha512", 
        password=converted_to_bytes_password_hash, salt=converted_to_bytes_salt, iterations=NUMBER_OF_HASH_ITERATIONS, dklen=32)
    
    #convert bytes after hash function to base64 
    result = base64.b64encode(additionaly_hashed_master_password) 
    
    #convert base64 bytes to string
    result = result.decode()
    
    return result