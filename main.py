#!/usr/bin/env python3

from pathlib import Path

from argparse import ArgumentParser
from bs4 import BeautifulSoup

def main():
    parser = ArgumentParser()
    parser.add_argument("rss")
    parser.add_argument("media")
    parser.add_argument("server")
    args = parser.parse_args()
    print(f"Server is {args.server}")
    mediaStems = list()
    mediaPaths = list()
    for item in Path(args.media).iterdir():
        mediaStems.append(item.stem)
        mediaPaths.append(item)
    with open(args.rss) as file:
        rssContents = file.read()
    soup = BeautifulSoup(rssContents, "lxml-xml") # lxml installed from pip     
    rssItems = soup.find_all("item")
    for item in rssItems:
        if item.title.string in mediaStems:
            mediaId = mediaStems.index(item.title.string)
            # print(item.enclosure.get("url"))
            item.enclosure["url"] = args.server + mediaPaths[mediaId].as_posix()
            # print(item.enclosure["url"])
        else:
            print(f"Couldn't find {item.title.string}")
    with open(args.rss, "w", encoding='utf-8') as file:
        file.write(str(soup))


if __name__ == "__main__":
    main()
