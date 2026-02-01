from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class ReleaseFileEntry:
    hashsum: str
    size_bytes: int
    filename: str


class ReleaseFile:
    def __init__(self):
        self.origin: str
        self.label: str
        self.suite: str
        self.version: str
        self.codename: str
        self.date: str
        self.architectures: Set[str]
        self.components: Set[str]
        self.description: str
        self.acquire_by_hash: bool
        self.md5sum: Dict[str, ReleaseFileEntry] = {}
        self.sha1sum: Dict[str, ReleaseFileEntry] = {}
        self.sha256sum: Dict[str, ReleaseFileEntry] = {}

    def has_archs(self, arch: List[str]) -> bool:
        arch_set = set(arch)
        intersected = self.architectures.intersection(arch_set)

        return len(arch) == len(intersected)

    def has_components(self, components: List[str]) -> bool:
        components_set = set(components)
        intersected = self.components.intersection(components_set)

        return len(components) == len(intersected)
    
    def has_file(self, filename: str) -> Optional[ReleaseFileEntry]:
        if filename in self.sha256sum:
            return self.sha256sum[filename]
        return None


def parse_release(content: str) -> ReleaseFile:
    out = ReleaseFile()
    current_hash: Optional[str] = None
    for line in content.splitlines():
        line: str
        if line.startswith(" "):
            if current_hash == None:
                raise RuntimeError(
                    "Encountered hash line but no hash type was recorded"
                )
            hashsum, size_bytes, filename = line.split()
            entry = ReleaseFileEntry(
                hashsum=hashsum, size_bytes=int(size_bytes), filename=filename
            )
            if current_hash == "md5":
                out.md5sum[entry.filename] = entry

            elif current_hash == "sha1":
                out.sha1sum[entry.filename] = entry

            elif current_hash == "sha256":
                out.sha256sum[entry.filename] = entry

            else:
                raise RuntimeError(f"Encountered unknown hash type: {current_hash}")
        elif line.lower().startswith("origin"):
            out.origin = line.split(": ")[1]

        elif line.lower().startswith("label"):
            out.label = line.split(": ")[1]

        elif line.lower().startswith("suite"):
            out.suite = line.split(": ")[1]

        elif line.lower().startswith("version"):
            out.version = line.split(": ")[1]

        elif line.lower().startswith("codename"):
            out.codename = line.split(": ")[1]

        elif line.lower().startswith("date"):
            out.date = line.split(": ")[1]

        elif line.lower().startswith("architectures"):
            out.architectures = set(line.split(": ")[1].split(" "))

        elif line.lower().startswith("components"):
            out.components = set(line.split(": ")[1].split(" "))

        elif line.lower().startswith("description"):
            out.description = line.split(": ")[1]

        elif line.lower().startswith("acquire-by-hash"):
            out.acquire_by_hash = True if line.split(": ")[1] == "yes" else False

        elif line.lower().startswith("md5"):
            current_hash = "md5"

        elif line.lower().startswith("sha256"):
            current_hash = "sha256"

        elif line.lower().startswith("sha1"):
            current_hash = "sha1"
        else:
            raise RuntimeError(f"Encountered unknown tag in a line: {line}")
    return out
