from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from PIL import Image
import os
import uuid
import subprocess

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/generate")
async def generate(data: TextInput):
    text = data.text
    uid = str(uuid.uuid4())

    # 1. Voice Generate
    tts = gTTS(text)
    tts_path = f"{uid}.mp3"
    tts.save(tts_path)

    # 2. Resize background image
    image = Image.open("bg.jpg")
    image = image.resize((1280, 720))
    img_path = f"{uid}.png"
    image.save(img_path)

    # 3. Generate video using ffmpeg
    video_path = f"{uid}.mp4"
    cmd = f"ffmpeg -loop 1 -i {img_path} -i {tts_path} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {video_path} -y"
    subprocess.call(cmd, shell=True)

    return {"video_url": f"http://localhost:8000/video/{video_path}"}

@app.get("/video/{filename}")
async def serve_video(filename: str):
    return FileResponse(filename, media_type="video/mp4", filename=filename)
