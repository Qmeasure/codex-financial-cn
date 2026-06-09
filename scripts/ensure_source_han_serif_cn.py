#!/usr/bin/env python3
"""Ensure Source Han Serif CN Regular/Bold are available for artifact checks."""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

FONT_FAMILY = "Source Han Serif CN"
FONT_FILES = {
    "SourceHanSerifCN-Regular.otf": "https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/SubsetOTF/CN/SourceHanSerifCN-Regular.otf",
    "SourceHanSerifCN-Bold.otf": "https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/SubsetOTF/CN/SourceHanSerifCN-Bold.otf",
}


def user_font_dir() -> Path:
    system = platform.system()
    home = Path.home()
    if system == "Darwin":
        return home / "Library" / "Fonts"
    if system == "Windows":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "Microsoft" / "Windows" / "Fonts"
        return home / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts"
    return home / ".local" / "share" / "fonts"


def fontconfig_matches() -> bool:
    fc_match = shutil.which("fc-match")
    if not fc_match:
        return False
    try:
        proc = subprocess.run(
            [fc_match, FONT_FAMILY],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        return False
    return FONT_FAMILY in proc.stdout


def installed_files_exist(font_dir: Path) -> bool:
    return all((font_dir / filename).is_file() for filename in FONT_FILES)


def download_fonts(font_dir: Path) -> None:
    font_dir.mkdir(parents=True, exist_ok=True)
    for filename, url in FONT_FILES.items():
        target = font_dir / filename
        if target.is_file() and target.stat().st_size > 0:
            continue
        print(f"installing {filename} from Adobe Source Han Serif release")
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        if len(data) < 1_000_000:
            raise RuntimeError(f"downloaded font is unexpectedly small: {filename}")
        target.write_bytes(data)


def refresh_font_cache() -> None:
    fc_cache = shutil.which("fc-cache")
    if not fc_cache:
        return
    subprocess.run([fc_cache, "-f"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    font_dir = user_font_dir()
    if fontconfig_matches() or installed_files_exist(font_dir):
        print(f"OK — {FONT_FAMILY} font is available.")
        return 0
    try:
        download_fonts(font_dir)
        refresh_font_cache()
    except Exception as exc:
        print(f"FAIL: cannot install {FONT_FAMILY}: {exc}", file=sys.stderr)
        return 1
    if not (fontconfig_matches() or installed_files_exist(font_dir)):
        print(f"FAIL: {FONT_FAMILY} was installed but cannot be verified", file=sys.stderr)
        return 1
    print(f"OK — installed {FONT_FAMILY} Regular/Bold in {font_dir}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
