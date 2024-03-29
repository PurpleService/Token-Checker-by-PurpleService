__author__ = "Lacoste with love for PurpleService (https://discord.gg/purple-service)"

from typing import Generator
from os import system, path

import sys
import aiohttp

if sys.version_info < (3, 7):
    exit(f"Python version ({sys.version}) dont support asyncio syntax used in this script.\n\nPlease update to Python 3.7>=.")

import asyncio

q = "\033[35m[?]\033[0m "
x = "\033[91m[X]\033[0m "
i = "\033[35m[!]\033[0m "

def cls() -> None:
    if sys.platform in ('win32'): 
        return system('cls') 
    return system('clear')

class TokenCheker:
    def __init__(self) -> None:
        self.accounts_working: list = []
        self.accounts_not_working: list = []

        self.counter_working: int = 0
        self.counter_not_working: int = 0

        self._requests_count: int = 0
        self._rate_limit: int = 60
        self._is_rate_limit: bool = False

    @property
    def discord_api(self) -> str:
        return "https://discordapp.com/api/"

    @staticmethod
    def headers(token: str) -> dict:
        return {"authorization": token}

    def load_tokens(self, fpath: str) -> Generator[str, None, None]:
        tokens = 0
        with open(fpath, "r") as f:
            for line in f.readlines():
                line = line.replace(" ", "")
                line = line.replace("\r", "")
                line = line.replace("\n", "")

                if not line:
                    continue

                tokens += 1

                yield line

    async def check_token(self, token: str) -> None:
        """This function will try login into discord api using token,

        This function will respect discord rate limit: `60` per sec.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.discord_api}v6/users/@me/library", headers=self.headers(token)) as r:
                if r.status == 200: # when token is valid.
                    self.accounts_working.append(token)
                    self.counter_working += 1
                    return

            self.counter_not_working += 1
            self.accounts_not_working.append(token)

    async def _run(self) -> None:
        tasks: list = []
        cls()
        for token in self.load_tokens(q2): 
            self._requests_count += 1

            if self._requests_count >= self._rate_limit:
                print(i, "\nRate limit was active waiting 1 second...\n")
                self._requests_count = 0
                await asyncio.sleep(1)

            tasks.append(asyncio.create_task(self.check_token(token)))
            print("{}Total checked: {} | Working: {} | Not Working: {}".format(i, self.counter_working + self.counter_not_working, self.counter_working, self.counter_not_working), end="\r")
        await asyncio.wait(tasks)
        print("{}Total checked: {} | Working: {} | Not Working: {}".format(i, self.counter_working + self.counter_not_working, self.counter_working, self.counter_not_working))

if __name__ == '__main__':
    cls()
    print(f"Discord Token Cheker 1.0\nMade By: {__author__}\n\n")
    q2 = input("{}Which tokens do you want check?[file.txt]: ".format(q))

    if not path.exists(q2):
        while True:
            q2 = input("{}Please put some valid file!: ".format(x))
            if path.exists(q2):
                break

    q1 = input("{}Want to save all the worked tokens at a txt file?[Y/N]: ".format(q)).lower()

    if q1 == "y":
        q3 = input("{}What file u want to save?[file.txt]: ".format(q))
        if not path.exists(q2):
            while True:
                q3 = input("{}Please put some valid file!: ".format(x))
                if path.exists(q2):
                    break

    token_cheker = TokenCheker()

    asyncio.run(token_cheker._run())

    if q1 == "y":
        with open(q3, 'w+') as f:
            for working in token_cheker.accounts_working:
                f.write("{}\n".format(working))
