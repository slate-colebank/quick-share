from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

@app.route("/")

def index():
    # return "<p>Hello, World</p>"
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected file'}), 400

    uploaded = []
    for file in files:
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded.append(filename)

        return jsonify({
            'message': f'uploaded file(s)',
            'files': uploaded
        }), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)
