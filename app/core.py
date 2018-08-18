
from werkzeug.utils import secure_filename

from model.utils.image import greyscale, crop_image, pad_image, \
    downsample_image, TIMEOUT

from scipy.misc import imread

import PIL
from PIL import Image

from loader import model 
import os

UPLOAD_FOLDER = os.path.dirname('/tmp/')

from flask import Flask
from flask import render_template, request, send_from_directory

app = Flask(__name__)
	
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'GET': 
		return render_template('index.html')

	if request.method == 'POST':
	    file = request.files['image']
	    filename = secure_filename(file.filename)
	    savedpath = os.path.join(UPLOAD_FOLDER, filename)
	    file.save(savedpath)
	    print("New uploaded file: [%s]" % savedpath)

	    try:

	    	if filename[-3:] == "png":

	        	img = imread(savedpath)

	    	elif filename[-3:] == "pdf":
	                # call magick to convert the pdf into a png file
	        	buckets = [
	            	[240, 100], [320, 80], [400, 80], [400, 100], [480, 80], [480, 100],
	            	[560, 80], [560, 100], [640, 80], [640, 100], [720, 80], [720, 100],
	            	[720, 120], [720, 200], [800, 100], [800, 320], [1000, 200],
	            	[1000, 400], [1200, 200], [1600, 200], [1600, 1600]
	        	]

	        	dir_output = "tmp/"
	        	name = savedpath.split('/')[-1].split('.')[0]

	        	run("magick convert -density {} -quality {} {} {}".format(200, 100,
					savedpath, dir_output+"{}.png".format(name)), TIMEOUT)
	        	savedpath = dir_output + "{}.png".format(name)
	        	crop_image(savedpath, savedpath)
	        	pad_image(savedpath, savedpath, buckets=buckets)
	        	downsample_image(savedpath, savedpath, 2)

	        	img = imread(savedpath)
	        else:
	        	raise "Unsupported file format"
	       	img = greyscale(img)
	       	hyps = model.predict(img)
	       	model.logger.info(hyps[0])
	       	message = hyps[0]

	    except Exception as e:
	    	print(e)
	    	message = "Error loading. Try a different image"

	    return render_template('index.html', latexstr=message, filename=file.filename)

	return "NOT Support Method"

@app.route('/saved/<filename>')
def send_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

