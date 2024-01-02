import sys
import os
import json
import re
import html
import urllib
from pathlib import Path

import logging
logger = logging.getLogger()

import feedparser
from dateutil import parser


from datetime import datetime

def convert_date_format(date_str):
    # Define the format of the original date string (common in RSS feeds)
    original_format = "%a, %d %b %Y %H:%M:%S GMT"

    # Parse the original date string
    try:
        parsed_date = datetime.strptime(date_str, original_format)
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

    # Define the desired output format
    output_format = "%Y.%m.%d %H:%M"

    # Convert the parsed date to the desired format
    return parsed_date.strftime(output_format)



def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    return feed.entries


def fetch(url):
    # url = args.get("--url", None)

    #TODO: I fucked it up... This regular expression matches the beginning of URLs with either "http://" or "https://" and will also match if "www." is present after the protocol.
    matched = re.match("https?:\/\/(?:www\.)?", url)
    if matched is None:
        logger.error("URL seems improperly formatted")
        return


    entries = fetch_rss_feed(url)

    if len(entries) == 0:
        logger.error("Given RSS feed has no entries")
        return

    # Sort entries by published date
    entries.sort(key=lambda entry: parser.parse(entry.published))

    # print(entries)
    print(len(entries))
    return entries

    # try:
    #     next_newest_article = entries[0]  # Post the first article if no last_processed_article found
    # except IndexError:
    #     logger.error("Unable to find any articles")
    #     sys.exit(1)

    # print(f"{next_newest_article.title}\n\n{next_newest_article.link}")




# https://github.com/PlebeiusGaragicus/nosrss/blob/main/nosrss/commands/fetch.py
# https://bitcoinmagazine.com/.rss/full/
# https://feeds.bbci.co.uk/news/world/rss.xml
a = fetch("https://bitcoinmagazine.com/.rss/full/")



for e in a:
    # print(e.title)
    # print(e.description)
    # print(e.content)

    # print(e.keys())

    date = convert_date_format(e.published).split(" ")[0]
    filename = f"./bitcoinmagazine/{date} {e.title}.txt"
    with open(filename, "w") as f:
        f.write(e.link)
        f.write("\n\n")
        f.write(e.title)
        f.write("\n")
        f.write(convert_date_format(e.published))
        f.write("\n\n")
        for c in e.content:
            f.write(c.value)


exit(0)

# save to text file
with open('rsses.txt', 'w') as file:
    for entry in a:
        file.write(f"{entry.title}\n\n{entry.link}\n\n\n\n")


