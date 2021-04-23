import asyncio
import webbrowser

import aiohttp
from bs4 import BeautifulSoup, Tag


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
    # print(data, file=open("result.html", "w"))
    # webbrowser.open("result.html")
    soup = BeautifulSoup(data, "lxml")
    result: Tag = soup.select_one(".kno-rdesc > span:nth-child(2)")
    print(result.text)
