#!/usr/bin/env python3
"""Download Lucide icons (ISC licence) into src/icons.json so pages can inline them.

Usage:  python3 src/fetch_icons.py plane wind cpu ...
Icon names: https://lucide.dev/icons
"""
import json, os, re, sys, urllib.request

VERSION = "0.460.0"
HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "icons.json")


def fetch(name):
    url = f"https://unpkg.com/lucide-static@{VERSION}/icons/{name}.svg"
    with urllib.request.urlopen(url, timeout=20) as r:
        svg = r.read().decode("utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S)
    return re.sub(r"\s*\n\s*", "", inner).strip()


def main(names):
    icons = json.load(open(STORE)) if os.path.exists(STORE) else {}
    for n in names:
        if n in icons:
            continue
        try:
            icons[n] = fetch(n)
            print("added", n)
        except Exception as e:  # noqa: BLE001
            print("FAILED", n, e)
    json.dump(dict(sorted(icons.items())), open(STORE, "w"), indent=0)


if __name__ == "__main__":
    main(sys.argv[1:])
