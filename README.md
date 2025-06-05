# Spotify Playlist Downloader

This repository provides a small command line utility for downloading entire Spotify playlists using the `spotdl` CLI. The script accepts a playlist URL and optional parameters to control the output directory, folder name and cookies file for YouTube Music authentication. After downloading, all tracks are archived into a zip file stored in a temporary directory.

```
python main.py PLAYLIST_URL [--output-dir downloads] [--folder-name NAME] [--cookies path/to/cookies.txt]
```

All files are downloaded directly to the specified directory and a temporary zip archive is created containing the playlist contents.
