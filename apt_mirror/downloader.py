from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
import urllib.parse
import requests

from apt_mirror.tools import join_url
from result import Result


class Downloader(ABC):
    @abstractmethod
    def get(self, *args: str) -> Result[bytes, int]:
        pass


class RequestsDownloader(Downloader):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, *args: str) -> Result[bytes, int]:
        if len(args) == 0:
            raise RuntimeError("Not enough url parts")
        full_url = join_url(self.base_url, *args)

        print(f"Getting {full_url}")

        response = requests.get(full_url)

        if response.status_code != 200:
            return Result.err(response.status_code)

        return Result.ok(response.content)
