from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
import urllib.parse
import requests

from tools import join_url
from result import Result


class Downloader(ABC):
    @abstractmethod
    def get_url(self, url: str) -> Result[bytes, int]:
        pass

    @abstractmethod
    def get(self, *args: str) -> Result[bytes, int]:
        pass

    @abstractmethod
    def to_file(self, file: str, *args: str) -> Result[None, int]:
        pass

class RequestsDownloader(Downloader):
    def __init__(self, base_url: str, user_agent: str):
        self.base_url = base_url
        self.headers = {"User-Agent": user_agent}

    def get_url(self, url: str) -> Result[bytes, int]:
        print(f"Getting {url}")

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return Result.err(response.status_code)

        return Result.ok(response.content)
    
    def get(self, *args: str) -> Result[bytes, int]:
        if len(args) == 0:
            raise RuntimeError("Not enough url parts")
        full_url = join_url(self.base_url, *args)

        print(f"Getting {full_url}")

        response = requests.get(full_url, headers=self.headers)

        if response.status_code != 200:
            return Result.err(response.status_code)

        return Result.ok(response.content)

    def to_file(self, file: str, *args: str) -> Result[None, int]:
        if len(args) == 0:
            raise RuntimeError("Not enough url parts")
        full_url = join_url(self.base_url, *args)

        print(f"Getting {full_url}")

        response = requests.get(full_url)

        if response.status_code != 200:
            return Result.err(response.status_code)

        return Result.ok(response.content)
