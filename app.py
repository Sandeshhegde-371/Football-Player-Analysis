from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from utils.convert_to_mp4 import convert_to_mp4  # Utility to convert .avi to .mp4
from main import main  # Your main processing function

# Initialize Flask app
app = Flask(__name__)

# Configuration for upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the homepage and handle file uploads."""
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            # Save the uploaded file
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_path)

            # Define paths for output files
            output_avi_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.avi')
            output_mp4_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp4')

            # Process the video using your main.py
            main(input_path, output_avi_path)

            # Convert AVI to MP4 for browser compatibility
            convert_to_mp4(output_avi_path, output_mp4_path)

            # Redirect to the video playback page
            return redirect(url_for('play_video', filename='output.mp4'))
    return render_template('index.html')


@app.route('/play/<filename>')
def play_video(filename):
    """Render a page to play the processed video."""
    video_url = url_for('download_file', filename=filename)
    return render_template('play_video.html', video_url=video_url)


@app.route('/download/<filename>')
def download_file(filename):
    """Provide a route to download the processed video."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
