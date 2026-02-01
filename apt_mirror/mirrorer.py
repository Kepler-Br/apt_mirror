import os
from packages_parser import parse_packages_gz
from release_parser import ReleaseFile, parse_release
from config import RepositoryConfig
from downloader import Downloader
from pathlib import Path
from abc import ABC, abstractmethod


class Mirrorer(ABC):
    @abstractmethod
    def run(self, repo_config: RepositoryConfig):
        pass


class AptMirrorer(Mirrorer):
    def __init__(
        self,
        downloader: Downloader,
    ):
        self.downloader = downloader

    def run(self, repo_config: RepositoryConfig):
        release_file = (
            self.downloader.get("dists", repo_config.distribution, "Release")
            .unwrap("Unable to get Release file. Code:", True)
            .decode()
        )
        parsed_release_file = parse_release(release_file)

        has_archs = parsed_release_file.has_archs(repo_config.architectures)
        has_comp = parsed_release_file.has_components(repo_config.components)
        if not has_archs:
            raise RuntimeError("Not all architectures are present in Release file")
        if not has_comp:
            raise RuntimeError("Not all components are present in Release file")

    def _create_repo_root(self, repo_config: RepositoryConfig, *args: str):
        pth = Path(repo_config.output)
        pth.mkdir(parents=True, exist_ok=True)

    def _mirror_component(
        self,
        component: str,
        arch: str,
        repo_config: RepositoryConfig,
        release_file: ReleaseFile,
    ):
        if repo_config.sources:
            raise RuntimeError("Sources are not supported yet")
        packages_path = f"{component}/binary-{arch}/Packages.gz"
        has_packages = release_file.has_file(packages_path)
        if not has_packages:
            raise RuntimeError(
                f"Could not find packages file: {packages_path} for repo {repo_config.name}"
            )
        packages_binary = self.downloader.get(
            component, f"binary-{arch}", "Packages.gz"
        ).unwrap(
            f"Could not get Packages.gz file for repo {repo_config.name}",
            include_error_value=True,
        )
        packages = parse_packages_gz(packages_binary)
        for package in packages:
            filepath = package.filename
        pass
