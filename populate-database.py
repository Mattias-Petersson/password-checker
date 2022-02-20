import sqlite3

# A table of 5 users with bad passwords, all of which are in my name.
# The bad passwords are taken from Wikipedia's 10,000 most common passwords
# https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords


def bad_users():
    c = db.cursor()
    c.execute(
        """
        INSERT INTO users(username, password, email)
        VALUES
            ("Mattias", "password1", "Mattias1@mail.com"),
            ("Mattias", "12345679", "Mattias2@mail.com"),
            ("Mattias", "starwars", "Mattias3@mail.com"),
            ("Mattias", "football", "Mattias4@mail.com"),
            ("Mattias", "qwertyuiop", "Mattias5@mail.com");
        """
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
bad_users()
