from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from apt_mirror.tools import join_url


@dataclass(frozen=True)
class RepositoryConfig:
    name: str
    reptype: str
    url: str
    components: List[str]
    distribution: str
    architectures: List[str]
    sources: bool
    output: str

    def path_to_file(self, file: str) -> str:
        return str(Path(self.output).joinpath(file))
    
    def url_to_file(self, *args: str) -> str:
        return join_url(self.url, *args)

    def url_to_file_component(self, distribution: str, arch: str, component: str) -> str:
        return join_url(self.url, "dists", distribution, )


@dataclass(frozen=True)
class MirrorProgramConfig:
    connections: int
    max_speed_bytes: int


@dataclass(frozen=True)
class MirrorConfig:
    config: MirrorProgramConfig
    repositories: List[RepositoryConfig]


def get_config(path: str) -> MirrorConfig:
    with open(path) as fp:
        data = yaml.safe_load(fp)

    loaded_repos: List[RepositoryConfig] = []

    for repo in data["repositories"]:
        config = RepositoryConfig(
            name=repo["name"],
            reptype=repo["type"],
            url=repo["url"],
            components=repo["components"].split(","),
            distribution=repo["distribution"],
            architectures=repo["architectures"].split(","),
            sources=repo["sources"],
            output=repo["output"],
        )
        loaded_repos.append(config)
    program_config = data["config"]
    cfg = MirrorProgramConfig(
        connections=int(program_config["connections"]),
        max_speed_bytes=int(program_config["max_speed"].replace("MB", "")),
    )

    return MirrorConfig(config=cfg, repositories=loaded_repos)
