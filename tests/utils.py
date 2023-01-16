import secrets
import requests
from hashlib import sha1
from uuid import uuid4


WORD_SITE = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(WORD_SITE)
words = response.content.splitlines()


def get_random_word():
    return secrets.choice(words).decode()


def get_random_email():
    return f"{get_random_word()}@gmail.com"


def get_random_word_hash():
    return sha1(secrets.choice(words)).hexdigest()


def get_random_id():
    return str(uuid4())

