
from app import app
import os

from flask import render_template, request, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.dirname('/tmp/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
  
    return render_template('index.html', latexstr="here should be the results", filename=file.filename)

@app.route('/saved/<filename>')
def send_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)