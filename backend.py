from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import yt_dlp
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Adjusted CORS origin to match frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cur_dir = os.getcwd()

@app.post("/download")
def download_video(link: str = Form(...)):
    youtube_dl_options = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(cur_dir, "%(title)s.%(ext)s"),
        "nocolor": True,
        "verbose": True
    }

    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        return {"message": "Download started successfully. Check your download folder."}
    except Exception as e:
        return {"message": f"An error occurred during download: {str(e)}"}
@app.get("/file/{file_name}")
async def get_file(file_name: str):
    file_path = Path(cur_dir) / file_name
    if file_path.exists():
        return FileResponse(path=file_path, filename=file_name, media_type="application/octet-stream")
    else:
        raise HTTPException(status_code=404, detail="File not found")