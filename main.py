from flask import Flask, request, send_file
from gtts import gTTS
import os
import uuid
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask Backend is Running!"

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("script")
    lang = request.form.get("language", "hi")
    bg_img = request.files.get("bg_image")
    bg_music = request.files.get("bg_music")

    uid = str(uuid.uuid4())
    os.makedirs(f"static/{uid}", exist_ok=True)

    bg_img_path = f"static/{uid}/bg.jpg"
    bg_music_path = f"static/{uid}/music.mp3"
    audio_path = f"static/{uid}/voice.mp3"
    video_path = f"static/{uid}/video.mp4"

    if bg_img:
        bg_img.save(bg_img_path)
    if bg_music:
        bg_music.save(bg_music_path)

    tts = gTTS(text, lang=lang)
    tts.save(audio_path)

    cmd = f'ffmpeg -loop 1 -i {bg_img_path} -i {audio_path} -i {bg_music_path} -shortest -y -vf "scale=1280:720" {video_path}'
    subprocess.call(cmd, shell=True)

    return send_file(video_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
