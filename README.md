# Spotify Playlist Downloader

This repository provides a small command line utility for downloading entire Spotify playlists using the `spotdl` CLI. The script accepts a playlist URL and optional parameters to control the output directory, folder name and cookies file for YouTube Music authentication.

```
python main.py PLAYLIST_URL [--output-dir downloads] [--folder-name NAME] [--cookies path/to/cookies.txt]
```

All files are downloaded directly to the specified directory without any subfolders.
