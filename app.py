from flask import Flask, render_template, request, jsonify, send_file
import os
import subprocess

app = Flask(__name__, template_folder="templates")

# Folder for downloaded videos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def extract_video_segment(url, output_path, start_time, duration):
    """Extract a segment from YouTube video without downloading the full video."""
    try:
        # Base yt-dlp command
        ytdlp_cmd = ["yt-dlp", "-f", "b", "-g", url]

        # Add cookies if file exists and is not empty
        cookies_file = "cookies.txt"
        if os.path.isfile(cookies_file) and os.path.getsize(cookies_file) > 0:
            ytdlp_cmd = ["yt-dlp", "--cookies", cookies_file, "-f", "b", "-g", url]

        # Get raw video stream URL
        raw_url = subprocess.check_output(ytdlp_cmd, stderr=subprocess.DEVNULL).decode().strip()

        # Command to extract only the requested portion
        command = [
            "ffmpeg", "-ss", str(start_time), "-i", raw_url,
            "-t", str(duration), "-c", "copy", output_path, "-y"
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        raise RuntimeError(f"Error extracting video: {e}")

@app.route("/")
def home():
    """Display home page with form."""
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_video():
    """Extract the requested portion of the YouTube video."""
    url = request.form.get("url")
    start_time = int(request.form.get("start"))  # Time in seconds
    end_time = int(request.form.get("end"))      # Time in seconds

    if not url or start_time is None or end_time is None:
        return jsonify({"error": "All fields are required."}), 400

    duration = end_time - start_time
    if duration <= 0:
        return jsonify({"error": "End time must be greater than start time."}), 400

    video_id = url.split("=")[-1]
    output_file = os.path.join(DOWNLOAD_FOLDER, f"{video_id}_cut.mp4")

    try:
        extract_video_segment(url, output_file, start_time, duration)
        return jsonify({"download_link": f"/video/{video_id}_cut.mp4"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/video/<filename>")
def serve_video(filename):
    """Serve the trimmed video for download."""
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

