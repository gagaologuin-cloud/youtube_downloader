import os
from flask import Flask, request, jsonify
from pytubefix import YouTube

app = Flask(__name__)

DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

@app.route('/')
def home():
    return "✅ YouTube Downloader Web App is running!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    mode = data.get('mode', 'mp4')

    if not url:
        return jsonify({"status": "error", "message": "Missing YouTube URL"}), 400

    yt = YouTube(url)
    title = yt.title.replace("/", "_").replace("\\", "_")

    if mode == "mp3":
        stream = yt.streams.filter(only_audio=True).first()
        file_path = os.path.join(DOWNLOAD_PATH, f"{title}.mp3")
        temp_file = stream.download(output_path=DOWNLOAD_PATH)
        base, _ = os.path.splitext(temp_file)
        os.rename(temp_file, file_path)
    else:
        stream = yt.streams.get_highest_resolution()
        file_path = os.path.join(DOWNLOAD_PATH, f"{title}.mp4")
        stream.download(output_path=DOWNLOAD_PATH, filename=os.path.basename(file_path))

    return jsonify({
        "status": "success",
        "title": title,
        "file_path": file_path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
