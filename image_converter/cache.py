import hashlib
import json
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class CacheEntry:
    input_file: Path
    output_file: Path
    output_format: str
    quality: int
    key: str = field(init=False)

    def __post_init__(self):
        self.key = compute_hash_key(
            Path(self.input_file), self.output_format, self.quality
        )

    def to_dict(self):
        return {
            "input": str(self.input_file.resolve()),
            "output": str(self.output_file.resolve()),
            "output_format": str(self.output_format),
            "quality": self.quality,
        }


class Cache:
    def __init__(self, filename: str):
        self.path = Path(filename)

        if not self.path.suffix == ".json":
            raise ValueError("Cache file must be a .json file")

        if self.path.exists():
            with open(self.path, "r") as f:
                self.data = json.load(f)

        else:
            self.data = {}
            self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def lookup(self, key: str) -> bool:
        return key in self.data

    def add(self, entry: CacheEntry):
        if not self.lookup(entry.key):
            self.data[entry.key] = entry.to_dict()
            self._save()
            return entry
        else:
            return {
                "status": "skipped",
                "file": str(entry.input_file.resolve()),
                "reason": "Found in cache",
            }


def compute_hash_key(file_path: Path, output_format: str, quality: int):
    stat = file_path.stat()

    key_string = "|".join(
        [
            str(file_path.resolve()),
            str(stat.st_mtime),
            str(stat.st_size),
            output_format,
            str(quality),
        ]
    )

    return hashlib.sha256(key_string.encode()).hexdigest()
