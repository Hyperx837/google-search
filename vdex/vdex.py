import sys

import aiohttp
from bs4 import BeautifulSoup, Tag

if sys.platform == "linux":
    import subprocess

    def say(text: str):
        cmd = f"nanotts-git -i -v en-US --speed 0.8 --pitch 1.4 -w -p ".split()
        cmd.insert(2, text)
        subprocess.call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


else:
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty("rate", 125)

    def say(text: str):
        engine.say(text)
        engine.runAndWait()


async def get_data(query: str) -> str:
    """get data required for processing"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://google.com/search?q={query}") as resp:
            return await resp.text()


async def main():
    """The main function of the package that puts everything together"""
    query = input("What do you want to search today? ")
    # query = "google"
    data = await get_data(query)
    soup = BeautifulSoup(data, "lxml")
    result: Tag = (
        soup.select_one(
            ".c2xzTb > div:nth-child(1) > div:nth-child(1) > \
        div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)"
        )
        or soup.select_one(".kno-rdesc > span:nth-child(2)")
        or soup.select_one(".g > div > div > div:nth-child(2) > span > span:last-child")
    )

    say(result.text)
