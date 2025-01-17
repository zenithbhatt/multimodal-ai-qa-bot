import os
import glob
from openai import OpenAI
import yt_dlp as youtube_dl
from yt_dlp import DownloadError
import docarray

openai_api_key = os.getenv("OPENAI_API_KEY")

youtube_url = "https://www.youtube.com/watch?v=aqzxYofJ_ck"
output_dir = "files/audio/"

# Config for youtube-dl
ydl_config = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
    "verbose": True
}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Downloading video from {youtube_url}")

try:
    with youtube_dl.YoutubeDL(ydl_config) as ydl:
        ydl.download([youtube_url])
except DownloadError:
    with youtube_dl.YoutubeDL(ydl_config) as ydl:
        ydl.download([youtube_url])


audio_file = glob.glob(os.path.join(output_dir, "*.mp3"))
audio_filename = audio_file[0]
print(audio_filename)

audio_file = audio_filename
output_file = "files/transcripts/transcripts.txt"
model = "whisper-1"

print("converting audio to text...")

with open(audio_file, "rb") as audio:
    response = OpenAI.audio.transcribe(model, audio)

transcript = (response["text"])

if output_file is not None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as file:
        file.write(transcript)

print(transcript)