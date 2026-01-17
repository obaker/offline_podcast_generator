#!/usr/bin/env python3

from pathlib import Path

from argparse import ArgumentParser
from bs4 import BeautifulSoup


def main():
    parser = ArgumentParser()
    parser.add_argument("rss")
    parser.add_argument("media")
    args = parser.parse_args()
    mediaStems: list[str] = list()
    mediaPaths: list[Path] = list()
    for item in Path(args.media).iterdir():
        mediaStems.append(item.stem)
        mediaPaths.append(item)
    with open(args.rss) as file:
        rssContents = file.read()
    soup = BeautifulSoup(rssContents, "lxml-xml")
    rssItems = soup.find_all("item")
    for item in rssItems:
        if item.title.string in mediaStems:
            mediaId = mediaStems.index(item.title.string)
            filename = item.find("acast:episodeUrl").contents[0]
            old_path = mediaPaths[mediaId].resolve()
            full_filename = Path(old_path.parent, filename + old_path.suffix)
            old_path.rename(full_filename)


if __name__ == "__main__":
    main()
