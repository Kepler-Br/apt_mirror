#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import sys
from typing import List
import yaml

from packages_parser import parse_packages_gz
from config import get_config
from downloader import Downloader, RequestsDownloader
from mirrorer import AptMirrorer, Mirrorer

try:
    import argcomplete
except ImportError:
    argcomplete = None


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    subparsers = p.add_subparsers(required=True)

    mirrorer = subparsers.add_parser("mirror", help="run mirroring tool")
    checker = subparsers.add_parser("check", help="check packages integrity")
    infoer = subparsers.add_parser("info", help="get info about mirrored repos")

    return p


def main():
    # with open("/home/kepler-br/Downloads/Packages.gz", 'rb') as fp:
    #     packages = parse_packages_gz(fp.read())
    #     print(len(packages))
    # return
    parsed = create_parser().parse_args()

    config = get_config("./../config.yaml")
    downloader = RequestsDownloader(config.repositories[0].url, config.config.user_agent)
    mirrorer = AptMirrorer(downloader)

    mirrorer.run(config.repositories[0])


if __name__ == "__main__":
    main()
