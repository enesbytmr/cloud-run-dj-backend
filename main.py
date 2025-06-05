#!/usr/bin/env python3

import os
import argparse
import subprocess
import tempfile
import shutil


def sanitize(s: str) -> str:
    """Remove characters invalid for filenames."""
    return "".join(c for c in s if c.isalnum() or c in " _-").rstrip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a Spotify playlist via the spotdl CLI."
    )
    parser.add_argument(
        "playlist",
        help="Spotify playlist URL",
    )
    parser.add_argument(
        "--output-dir",
        default="downloads",
        help="Base directory to save downloads",
    )
    parser.add_argument(
        "--folder-name",
        help="Name of the playlist folder (defaults to playlist ID)",
    )
    parser.add_argument(
        "--cookies",
        help="Path to cookies.txt file for YouTube Music authentication (optional)",
    )

    args = parser.parse_args()

    # Determine playlist folder name
    if args.folder_name:
        playlist_name = sanitize(args.folder_name)
    else:
        raw_name = args.playlist.rstrip("/").split("/")[-1].split("?")[0]
        playlist_name = sanitize(raw_name)

    base_dir = os.path.join(args.output_dir, playlist_name)
    os.makedirs(base_dir, exist_ok=True)

    output_template = os.path.join(base_dir)

    cmd = [
        "spotdl",
        args.playlist,
        "--output",
        output_template,
        "--audio",
        "youtube-music",
        "--format",
        "m4a",
        "--threads",
        "5",
    ]

    if args.cookies:
        cmd.extend(["--cookie-file", args.cookies])

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    temp_dir = tempfile.mkdtemp(prefix="spotdl_")
    archive_base = os.path.join(temp_dir, playlist_name)
    zip_path = shutil.make_archive(archive_base, "zip", base_dir)
    print("Created archive:", zip_path)


if __name__ == "__main__":
    main()
