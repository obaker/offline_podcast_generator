#!/usr/bin/env python3

from datetime import timedelta
from pathlib import Path

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from eyed3 import load as eyed3Load


def main():
    parser = ArgumentParser()
    parser.add_argument("rss")
    parser.add_argument("media")
    parser.add_argument("addr")
    args = parser.parse_args()
    mediaStems: list[str] = list()
    mediaPaths: list[Path] = list()
    for item in Path(args.media).iterdir():
        mediaStems.append(item.stem)
        mediaPaths.append(item)
    with open(args.rss) as file:
        rssContents = file.read()
    soup = BeautifulSoup(rssContents, "lxml-xml")  # lxml installed from pip
    rssItems = soup.find_all("item")
    for item in rssItems:
        if item.title.string in mediaStems:
            mediaId = mediaStems.index(item.title.string)
            item.enclosure["url"] = args.addr + mediaPaths[mediaId].as_posix()
            audiofile = eyed3Load(mediaPaths[mediaId]).info
            item.enclosure["length"] = audiofile.size_bytes
            length: str = str(timedelta(seconds=round(audiofile.time_secs)))
            item.find("itunes:duration").contents = length
        else:
            item.decompose()
    with open(args.rss, "w", encoding='utf-8') as file:
        file.write(str(soup))


if __name__ == "__main__":
    main()
