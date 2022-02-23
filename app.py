from urllib.request import urlopen
import re
import hashlib
import sqlite3


def scrapePasswords():
    url = "https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    # TODO:
    # fix regex-expression to only take passwords of length 8 or larger (passwords are assumed to be 8-characters or longer upon registration)
    # fix regex-expression to remove the last rows of the Wikipedia entry. There are spaces in all of those entries.
    regex_pattern = "<li>(.*)<\/li>"
    matches = re.findall(regex_pattern, html, re.IGNORECASE)
    # Could not do this in a for-loop, required iterating over the list twice. The variable the list points to is just a copy of the value, the changes weren't reflected.
    # Removes all the HTML-tags.
    matches = [re.sub("<.*?>", "", i) for i in matches]
    # Hashes them in the same way that they are hashed locally.
    hashedPasswords = [hashlib.sha256(i.encode()).hexdigest() for i in matches]
    return set(hashedPasswords)


def getLocalData():
    db = sqlite3.connect("users-db.sqlite")
    c = db.cursor()
    c.execute(
        """
        SELECT user_id, username, password, email FROM users;
        """
    )
    db.commit()
    return c.fetchall()


badPasswords = scrapePasswords()
localData = getLocalData()
localPasswords = set([i[2] for i in localData])
# O(n) time complexity, however no indices of where the users are.
badPasswordsLocal = localPasswords.intersection(badPasswords)
if(badPasswordsLocal):
    for user_id, username, password, email in localData:
        if(password in badPasswordsLocal):
            print("User id: {0} \n Username: {1}, Email: {2}".format(
                user_id, username, email))
            print("____________")
