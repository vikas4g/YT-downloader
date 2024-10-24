from flask import Flask, render_template, request, redirect, jsonify
# from downloader import get_video_info, download_video, progress
from downloader import download_video, progress

import os

app = Flask(__name__)

# Create download directory if it doesn't exist
if not os.path.exists('download'):
    os.makedirs('download')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    
    try:
        download_video(url, format_type)
        return jsonify({"message": "Download started"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}"})

@app.route('/progress')
def get_progress():
    return jsonify(progress)

if __name__ == "__main__":
    app.run(debug=True)
