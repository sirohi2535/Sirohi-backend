
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from PIL import Image

from flask import Flask, request, send_file
from gtts import gTTSU nano 6.2                                                                         main.py

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from PIL import image
from flask import Flask, request, send_file
from gtts import gTTS
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

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("script")
    lang = request.form.get("language", "hi")
    bg_img = request.files.get("bg_image")
    bg_music = request.files.get("bg_music")

    uid = str(uuid.uuid4())
    os.makedirs(f"static/{uid}", exist_ok=True)

    # Save files
    bg_img_path = f"static/{uid}/bg.jpg"
    bg_music_path = f"static/{uid}/music.mp3"
    audio_path = f"static/{uid}/voice.mp3"
    video_path = f"static/{uid}/video.mp4"

    if bg_img:
        bg_img.save(bg_img_path)
    if bg_music:
        bg_music.save(bg_music_path)

    # Text to voice
    tts = gTTS(text, lang=lang)
    tts.save(audio_path)

    # Make video with ffmpeg
    cmd = f'ffmpeg -loop 1 -i {bg_img_path} -i {audio_path} -i {bg_music_path} -shortest -y -vf "scale=1280:720" {video_path}'
    subprocess.call(cmd, shell=True)

    return send_file(video_path, as_attachment=True)

app.run(host="0.0.0.0", port=5000)


from flask import Flask, request, send_file
from gtts import gTTS
from moviepy.editor import *
import os
import uuid

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("text")
    lang = request.form.get("lang")
    image = request.files.get("image")
    music = request.files.get("music")

    # Unique filenames
    uid = str(uuid.uuid4())
    audio_path = f"audio_{uid}.mp3"
    image_path = f"image_{uid}.png"
    music_path = f"music_{uid}.mp3"
    output_path = f"video_{uid}.mp4"

    # 1. Text to speech
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)

    # 2. Save uploaded files
    image.save(image_path)
    music.save(music_path)

    # 3. Create video
    clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)
    clip = clip.set_audio(CompositeAudioClip([
        AudioFileClip(audio_path).volumex(1.5),
        AudioFileClip(music_path).volumex(0.2)
    ]))
    clip.write_videofile(output_path, fps=24)

    # 4. Send video file
    return send_file(output_path, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

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

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("script")
    lang = request.form.get("language", "hi")
    bg_img = request.files.get("bg_image")
    bg_music = request.files.get("bg_music")

    uid = str(uuid.uuid4())
    os.makedirs(f"static/{uid}", exist_ok=True)

    # Save files
    bg_img_path = f"static/{uid}/bg.jpg"
    bg_music_path = f"static/{uid}/music.mp3"
    audio_path = f"static/{uid}/voice.mp3"
    video_path = f"static/{uid}/video.mp4"

    if bg_img:
        bg_img.save(bg_img_path)
    if bg_music:
        bg_music.save(bg_music_path)

    # Text to voice
    tts = gTTS(text, lang=lang)
    tts.save(audio_path)

    # Make video with ffmpeg
    cmd = f'ffmpeg -loop 1 -i {bg_img_path} -i {audio_path} -i {bg_music_path} -shortest -y -vf "scale=1280:720" {video_path}'
    subprocess.call(cmd, shell=True)

    return send_file(video_path, as_attachment=True)

app.run(host="0.0.0.0", port=5000)


from flask import Flask, request, send_file
from gtts import gTTS
from moviepy.editor import *
import os
import uuid

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("text")
    lang = request.form.get("lang")
    image = request.files.get("image")
    music = request.files.get("music")

    # Unique filenames
    uid = str(uuid.uuid4())
    audio_path = f"audio_{uid}.mp3"
    image_path = f"image_{uid}.png"
    music_path = f"music_{uid}.mp3"
    output_path = f"video_{uid}.mp4"

    # 1. Text to speech
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)

    # 2. Save uploaded files
    image.save(image_path)
    music.save(music_path)

    # 3. Create video
    clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)
    clip = clip.set_audio(CompositeAudioClip([
        AudioFileClip(audio_path).volumex(1.5),
        AudioFileClip(music_path).volumex(0.2)
    ]))
    clip.write_videofile(output_path, fps=24)

    # 4. Send video file
    return send_file(output_path, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


