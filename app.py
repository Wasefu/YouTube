from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Cookies file ka path (Render ke server pe)
COOKIES_PATH = "cookies.txt"

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    if not os.path.exists(COOKIES_PATH):
        return jsonify({"error": "Cookies file not found"}), 500

    try:
        ydl_opts = {
            "format": "best",
            "cookies": COOKIES_PATH
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"title": info["title"], "url": info["url"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
