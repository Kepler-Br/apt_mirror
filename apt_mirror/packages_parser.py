from dataclasses import dataclass
import gzip
from typing import List


class PackageEntry:
    md5sum: str
    sha1sum: str
    sha512sum: str
    size_bytes: int
    package_name: str
    architecture: str
    filename: str


def _validate_package_entry(val: PackageEntry):
    if val.md5sum is None:
        raise RuntimeError("md5sum is None")

    elif val.sha1sum is None:
        raise RuntimeError("sha1sum is None")

    elif val.sha512sum is None:
        raise RuntimeError("sha512sum is None")

    elif val.size_bytes is None:
        raise RuntimeError("size_bytes is None")

    elif val.package_name is None:
        raise RuntimeError("package_name is None")

    elif val.architecture is None:
        raise RuntimeError("architecture is None")

    elif val.filename is None:
        raise RuntimeError("filename is None")


def parse_packages_gz(packages_gz: bytes) -> List[PackageEntry]:
    decompressed = gzip.decompress(packages_gz)
    return parse_packages(decompressed)


def parse_packages(packages: bytes) -> List[PackageEntry]:
    entries: List[PackageEntry] = []
    current_package_entry: PackageEntry = PackageEntry()
    for line in packages.splitlines():
        decoded_line = line.decode()
        splitted_line = decoded_line.split(": ", maxsplit=1)
        # Entry: value
        if len(splitted_line) == 2:
            entry_name_lower, entry_value = (
                splitted_line[0].strip().lower(),
                splitted_line[1].strip(),
            )

            if entry_name_lower.startswith("md5sum"):
                current_package_entry.md5sum = entry_value

            elif entry_name_lower.startswith("sha1"):
                current_package_entry.sha1sum = entry_value

            elif entry_name_lower.startswith("sha512"):
                current_package_entry.sha512sum = entry_value

            elif entry_name_lower.startswith("size"):
                current_package_entry.size_bytes = int(entry_value)

            elif entry_name_lower.startswith("package"):
                current_package_entry.package_name = entry_value

            elif entry_name_lower.startswith("architecture"):
                current_package_entry.architecture = entry_value

            elif entry_name_lower.startswith("filename"):
                current_package_entry.filename = entry_value

        # empty line that signales that new package begun
        elif len(splitted_line) == 1 and len(splitted_line[0]) == 0:
            _validate_package_entry(current_package_entry)
            entries.append(current_package_entry)
            current_package_entry = PackageEntry()
        else:
            raise RuntimeError(f"Unknown package entry: {decoded_line}")
    return entries
