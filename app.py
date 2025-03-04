from flask import Flask, render_template, request, url_for
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
FILENAME = 'image.jpg'  # Fixed filename
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], FILENAME)
            file.save(file_path)  # Overwrites old file

    # Append timestamp to prevent caching issues
    timestamp = int(time.time())
    image_url = url_for('static', filename=f'uploads/{FILENAME}') + f"?v={timestamp}"

    return render_template('index.html', image_url=image_url)

# This is required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
