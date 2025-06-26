from flask import Flask, request, send_file
from gtts import gTTS
import os
import uuid
import subprocess

app = Flask(__name__)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    text = request.form.get("text")
    lang = request.form.get("lang", "hi")
    image = request.files.get("image")
    music = request.files.get("music")

    uid = str(uuid.uuid4())
    os.makedirs("static", exist_ok=True)

    # File paths
    image_path = f"static/image_{uid}.png"
    music_path = f"static/music_{uid}.mp3"
    audio_path = f"static/audio_{uid}.mp3"
    video_path = f"static/video_{uid}.mp4"

    # Save inputs
    image.save(image_path)
    music.save(music_path)

    # Text to speech
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)

    # Create video with ffmpeg
    cmd = f'ffmpeg -loop 1 -y -i {image_path} -i {audio_path} -i {music_path} -shortest -vf "scale=1280:720" -c:v libx264 -pix_fmt yuv420p {video_path}'
    subprocess.call(cmd, shell=True)

    return send_file(video_path, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
