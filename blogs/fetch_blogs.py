#!/usr/bin/env python3
"""
Fetches all blog posts from akuity.io using the sitemap and creates a .md file for each.
Usage: python3 fetch_blogs.py
"""

import re
import time
import os
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urljoin
from html.parser import HTMLParser

BASE_URL = "https://akuity.io"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch(url, _redirects=0):
    if _redirects > 5:
        raise URLError("Too many redirects")
    req = Request(url, headers=HEADERS)
    try:
        with urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        if hasattr(e, "code") and e.code in (301, 302, 307, 308):
            location = e.headers.get("Location")
            if location:
                return fetch(urljoin(url, location), _redirects + 1)
        raise


def get_blog_urls():
    xml = fetch(SITEMAP_URL)
    root = ET.fromstring(xml)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for loc in root.findall(".//sm:loc", ns):
        url = loc.text.strip()
        # Match /blog/<slug> but not /blog itself
        if re.match(r"https://akuity\.io/blog/[^/]+/?$", url):
            urls.append(url)
    return urls


class BlogPostParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.date = ""
        self.body_lines = []
        self._in_h1 = False
        self._in_time = False
        self._capture = False
        self._skip_depth = 0
        self._SKIP = {"script", "style", "nav", "footer", "header"}

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        if self._skip_depth:
            return
        if tag == "h1":
            self._in_h1 = True
        if tag == "time":
            self._in_time = True
            d = dict(attrs)
            if "datetime" in d:
                self.date = d["datetime"][:10]
        if tag == "article":
            self._capture = True
        if self._capture and tag in ("h2", "h3", "h4"):
            self.body_lines.append(f"\n{'#' * int(tag[1])} ")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        if tag == "h1":
            self._in_h1 = False
        if tag == "time":
            self._in_time = False
        if tag == "article":
            self._capture = False
        if tag in ("p", "h2", "h3", "h4", "li", "blockquote"):
            self.body_lines.append("\n")

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_h1 and not self.title:
            self.title = text
        if self._in_time and not self.date:
            self.date = text
        if self._capture:
            self.body_lines.append(text)


def slug_from_url(url):
    return url.rstrip("/").split("/")[-1]


def to_markdown(slug, title, date, body_lines):
    body = "".join(body_lines).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return f"""---
title: "{title}"
date: {date}
source: {BASE_URL}/blog/{slug}/
---

# {title}

{body}
"""


def main():
    print(f"Reading sitemap from {SITEMAP_URL} ...")
    urls = get_blog_urls()
    print(f"Found {len(urls)} blog posts.\n")

    for url in urls:
        slug = slug_from_url(url)
        filepath = os.path.join(OUTPUT_DIR, slug + ".md")

        if os.path.exists(filepath):
            print(f"  [skip] {slug}.md")
            continue

        try:
            html = fetch(url)
            parser = BlogPostParser()
            parser.feed(html)

            title = parser.title or slug.replace("-", " ").title()
            date = parser.date or ""
            md = to_markdown(slug, title, date, parser.body_lines)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"  [ok]   {slug}.md  ({title[:60]})")
        except Exception as e:
            print(f"  [err]  {slug}: {e}")

        time.sleep(0.4)

    print("\nDone.")


if __name__ == "__main__":
    main()
