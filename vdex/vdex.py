import sys

import requests
from bs4 import BeautifulSoup, Tag

if sys.platform == "linux":
    import subprocess

    def say(text: str):
        print(text)
        cmd = f"nanotts-git -i -v en-US --speed 0.8 --pitch 1.4 -w -p ".split()
        cmd.insert(2, text)
        subprocess.call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.Popen("rm nanotts-output-*.wav", shell=True)


else:
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty("rate", 125)

    def say(text: str):
        engine.say(text)
        engine.runAndWait()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def process_data(data):
    soup = BeautifulSoup(data, "lxml")
    answer_selectors = [
        ".Z0LcW",
        "div.wDYxhc:nth-child(2) > div:nth-child(1) > div:nth-child(1)",
        ".kno-rdesc > span:nth-child(2)",
        ".g > div > div > div:nth-child(2) > span > span:last-child",
    ]
    for selector in answer_selectors:
        answer: Tag = soup.select_one(selector)
        if answer and answer.text:
            return answer.text


def main():
    """The main function of the package that puts everything together"""

    query = input("What do you want to search today? ")
    data = requests.get(f"https://google.com/search?q={query}", headers=headers).text
    answer = process_data(data)
    print(answer)
    if answer.endswith("..."):  # removes the last sentense if it's incompleted
        answer = ". ".join(answer.split(". ")[:-1])

    say(answer)
