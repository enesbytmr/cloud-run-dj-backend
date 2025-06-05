from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import csv
import tempfile
import yt_dlp
from ytmusicapi import setup
import zipfile
import uuid
import shutil

app = FastAPI()


@app.get("/login")
async def login():
    """Trigger OAuth login and save cookies to /tmp."""
    auth_path = os.path.join(tempfile.gettempdir(), "yt_auth.json")
    setup(filepath=auth_path)
    return {"cookies_saved": auth_path}

@app.post("/download")
async def download_csv(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = f"/tmp/{session_id}"
    os.makedirs(session_dir, exist_ok=True)

    contents = await file.read()
    csv_path = f"{session_dir}/list.csv"
    with open(csv_path, "wb") as f:
        f.write(contents)

    tracks = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            artist = row.get("artist") or row.get("Artist")
            title = row.get("title") or row.get("Title")
            if artist and title:
                tracks.append((artist.strip(), title.strip()))

    try:
        for artist, title in tracks:
            filename_base = f"{artist} - {title}"
            output_path_mp3 = os.path.join(session_dir, f"{filename_base}.mp3")
            if os.path.exists(output_path_mp3):
                print(f"Already exists: {filename_base}")
                continue

            search_query = f"ytsearch1:{filename_base}"
            output_template = os.path.join(session_dir, f"{filename_base}.%(ext)s")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_query])

        zip_path = f"/tmp/{session_id}.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_name in os.listdir(session_dir):
                if file_name.endswith(".mp3"):
                    zipf.write(os.path.join(session_dir, file_name), arcname=file_name)

        return FileResponse(zip_path, filename="downloaded_tracks.zip")

    finally:
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)