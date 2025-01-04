from flask import Flask, render_template, request, redirect, url_for
import hashlib
from Crypto.Hash import SHA3_256
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        sha256_hash = generate_hash(file_path, 'sha256')
        sha3_hash = generate_hash(file_path, 'sha3_256')
        return render_template('index.html', file_path=file_path, sha256_hash=sha256_hash, sha3_hash=sha3_hash)
    return redirect(request.url)

def generate_hash(file_path, algorithm):
    if algorithm == 'sha256':
        hash_func = hashlib.sha256()
    elif algorithm == 'sha3_256':
        hash_func = SHA3_256.new()
    else:
        raise ValueError(f'Unsupported hash type {algorithm}')

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
