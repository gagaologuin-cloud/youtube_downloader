from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    format_type = request.form.get('format')

    if not url:
        return "No URL provided", 400

    ydl_opts = {'outtmpl': '%(title)s.%(ext)s'}

    if format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        if format_type == 'mp3':
            filename = os.path.splitext(filename)[0] + ".mp3"

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("✅ YouTube Downloader Web App is running!")
    app.run(host='0.0.0.0', port=port)
