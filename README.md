# cloud-run-dj-backend

A small FastAPI application that converts a list of YouTube tracks from a CSV file into MP3 downloads.

## Running

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Endpoints

### `GET /login`
Starts an authentication flow using `ytmusicapi` and stores the resulting cookie file in `/tmp/yt_auth.json`.

### `POST /download`
Upload a CSV file containing `artist` and `title` columns. The server downloads the songs and returns a ZIP archive of MP3 files.
