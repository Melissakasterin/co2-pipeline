from hashlib import sha256
from datetime import datetime, timezone
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
FILES = (
    (
        "owid-co2-data.csv",
        "https://raw.githubusercontent.com/owid/co2-data/382ee6c662b0ece26e111f263b44c029afad7787/owid-co2-data.csv",
        "7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6",
    ),
    (
        "owid-co2-codebook.csv",
        "https://raw.githubusercontent.com/owid/co2-data/382ee6c662b0ece26e111f263b44c029afad7787/owid-co2-codebook.csv",
        "33b4f5e00efd58c7b83863f736beba1af4df946b43642b0400c3ec38648e0e8e",
    ),
)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_source_log(path: Path, filename: str, url: str, checksum: str) -> None:
    with path.open("a+", encoding="utf-8") as source_log:
        source_log.seek(0, os.SEEK_END)
        if source_log.tell():
            source_log.seek(source_log.tell() - 1)
            if source_log.read(1) != "\n":
                source_log.write("\n")
        source_log.write(
            f"{datetime.now(timezone.utc):%Y-%m-%d} {filename}: {url} (SHA-256: {checksum})\n"
        )


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    missing_files = [filename for filename, _, _ in FILES if not (RAW_DIR / filename).exists()]
    raw_dir_is_writable = (
        RAW_DIR.is_dir()
        and os.access(RAW_DIR, os.W_OK)
        and bool(RAW_DIR.stat().st_mode & 0o222)
    )
    if missing_files and not raw_dir_is_writable:
        raise SystemExit(
            "Cannot download missing file(s) because data/raw/ is not writable. "
            "Run `chmod -R u+w data/raw` first."
        )

    for filename, url, expected_checksum in FILES:
        path = RAW_DIR / filename
        if not path.exists():
            try:
                with urlopen(url, timeout=60) as response:
                    contents = response.read()
            except (OSError, URLError) as error:
                raise SystemExit(f"Could not download {filename}: {error}") from error

            checksum = sha256(contents).hexdigest()
            if checksum != expected_checksum:
                raise SystemExit(
                    f"Checksum mismatch for {filename}: expected {expected_checksum}, "
                    f"got {checksum}; file was not saved."
                )

            try:
                path.write_bytes(contents)
                append_source_log(RAW_DIR / "SOURCES.txt", filename, url, checksum)
            except OSError as error:
                raise SystemExit(f"Could not save {filename} or update SOURCES.txt: {error}") from error

        print(f"{filename}: {path.stat().st_size} bytes, SHA-256 {file_sha256(path)}")


if __name__ == "__main__":
    main()