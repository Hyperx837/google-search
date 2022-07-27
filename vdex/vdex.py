#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from colorama import Fore

from typing import Optional, Tuple
from urllib import parse
import requests

from bs4 import BeautifulSoup, Tag

blue = "\033[3;27m"
grey = '\033[0;248m'
nocolor="\033[0m"


query = " ".join(sys.argv[1:])

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

answer_selectors = {
        "div.wDYxhc:nth-child(2) > div.IZ6rdc": "",  # main paragraph
        ".Z0LcW": "",  # highlted result
        ".XDTKBd": "",  # main result
        ".hgKElc": ".yuRUbf > a",  # featured snippet
        ".kno-rdesc > span:nth-child(1)": "",
        ".kno-rdesc > span:nth-child(2)": "",  # sidebar result
        ".VwiC3b": ".yuRUbf > a",  # first result
}

def process_answer(answer: str) -> str:
    """remove last sentence if it's incomplete"""
    if not answer.endswith("..."):
        return answer

    # 8 characters doesn't make a meaningful sentence
    sentences = answer.split(". ")
    if len(sentences[-1]) < 8:
        sentences = sentences[:-1]

    return ". ".join(sentences)


def get_answer(soup) -> Tuple[str, str]:
    """get google results"""
    for ans_selector, link_selector in answer_selectors.items():
        answer: Tag = soup.select_one(ans_selector)
        if answer and answer.text:
            link: str = (
                soup.select_one(link_selector)["href"]
                if link_selector
                else ""
            )
            answer = process_answer(answer.text)
            return answer, link

    return answer, ""



def handle_query(query):
    escaped_query = parse.quote(query)
    url = f"https://google.com/search?q={escaped_query}"
    markup = requests.get(url, headers=headers).text
    soup = BeautifulSoup(markup, "lxml")
    return get_answer(soup)


def main():
    answer, link = handle_query(query)
    print(Fore.LIGHTCYAN_EX + link)
    print(Fore.LIGHTYELLOW_EX + answer)
    print(Fore.WHITE)

if __name__ == "__main__":
    main()
