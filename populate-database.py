import sqlite3
import hashlib
import string
import random


# Generates a random username of size (default 8) of random ascii letters (upper- and lowercase).
def id_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# A class to store a user with all the fields that will be in the SQL entry for a user.
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


# Creating a list of 100 users, and adding 5 entries that will be a match when we compare it to a list of common passwords.
def create_users():
    users = []
    for _ in range(100):
        # Storing an id as a variable, to use the same random sequence as username, password, and mail with the suffix @mail.com.
        # Not secure at all, however will likely not trigger a match with the list of common passwords to compare with later.
        temp = id_generator()
        password = hashlib.sha256(temp.encode()).hexdigest()
        users.append(User(temp, password, temp + "@mail.com"))

    # Replace a few of them with entries that should 'hit' when we check through the leak.
    users[13] = User("Mattias", hashlib.sha256(
        "password1".encode()).hexdigest(), "Mattias1@mail.com")
    users[37] = User("Mattias", hashlib.sha256(
        "12345679".encode()).hexdigest(), "Mattias2@mail.com")
    users[55] = User("Mattias", hashlib.sha256(
        "starwars".encode()).hexdigest(), "Mattias3@mail.com")
    users[73] = User("Mattias", hashlib.sha256(
        "football".encode()).hexdigest(), "Mattias4@mail.com")
    users[99] = User("Mattias", hashlib.sha256(
        "qwertyuiop".encode()).hexdigest(), "Mattias5@mail.com")
    c = db.cursor()
    for i in users:
        c.execute(
            """
            INSERT INTO users(username, password, email)
            VALUES
            (?, ?, ?)
            """, [i.username, i.password, i.email]
        )
    db.commit()


# Connect and force foreign key constraints
db = sqlite3.connect("users-db.sqlite")
c = db.cursor()
c.execute(
    """
        PRAGMA foreign_keys=ON;
        """
)
db.commit()
create_users()
