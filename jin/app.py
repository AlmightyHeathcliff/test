import os
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory

from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from PIL import Image
from subprocess import PIPE, run
import time

__author__ = 'akn'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = '/home/ashish/projects/DEEP/image-quality-assessment-master/src/tests/test_images/images/'

@app.route("/flowimg", methods=['POST'])
def flowimg():
	r = request
	global target
	# print('<<<<<<<<<')
	# print(request.files.getlist("file"))
	print(r)
	# convert string of image data to uint8
	nparr = np.fromstring(r.data, np.uint8)
	# decode image
	print(1)
	filename = 'testimage.jpg'
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	img = Image.fromarray(img, 'RGB')
	if not os.path.isdir(target):
		os.mkdir(target)
	img.save(target+filename)
	print(2)
	response = {'message': 'image received. size={}x{}'.format(12,12)}
	print(3)
	resultis = runindocker("test")
	print('<><><><.@')
	print(resultis)
	#return str(resultis)
	response = {resultis}
	# encode response using jsonpickle
	response_pickled = jsonpickle.encode(response)

	return Response(response=response_pickled, status=200, mimetype="application/json")



@app.route("/")
def index():
	return render_template("upload.html")

IMG_DIR = ''
@app.route("/upload", methods=["POST"])
def upload():
	global IMG_DIR
	target = os.path.join(APP_ROOT, 'images')
	print(target)
	IMG_DIR = target

	if not os.path.isdir(target):
		os.mkdir(target)

	#print(request.files.getlist("file"))
	filename=''
	for upload in request.files.getlist("file"):
		print(upload)
		print("{} is the file name".format(upload.filename))
		filename = upload.filename
		# This is to verify files are supported
		ext = os.path.splitext(filename)[1]
		print('------------------------'+ext)
		if (ext == ".jpg") or  (ext == ".png") or  (ext == ".jpeg"):
			print("File supported moving on...")
		else:
			render_template("Error.html", message="Files uploaded are not supported...")
		destination = "/".join([target, filename])
		print("Accept incoming file:", filename)
		print("Save it to:", destination)
		upload.save(destination)
		result = filecorrection()

	if filename=='':
		return render_template("Error.html")
	# return send_from_directory("images", filename, as_attachment=True)
	return result#render_template("complete.html", image_name=filename)


def filecorrection():

	 
	root = os.getcwd()
	os.chdir(os.path.join(os.getcwd(),IMG_DIR))
	Param = os.getcwd()
 
	from os import listdir
	from os.path import isfile, join
	onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]



	for i in onlyfiles:
		file = i.split('.')
		print(file[1])
		os.rename(i,file[0]+'.jpg')
	print(os.system('dir'))
	print('outta rename')
	os.chdir(root)
	return runindocker(Param)

def runindocker(directoryuri):
	global target
	toPath = r"/home/ashish/projects/DEEP/image-quality-assessment-master/src/tests/test_images"
	if directoryuri!="test":
		fromPath = directoryuri
		os.system('sudo mv  {}/ {}/'.format(fromPath,toPath))
		time.sleep(6)

	os.chdir('/home/ashish/projects/DEEP/image-quality-assessment-master/')
	xxx=os.getcwd()
	print(xxx)
	cmd = 'sudo ./predict --docker-image nima-cpu --base-model-name MobileNet --weights-file $(pwd)/models/MobileNet/weights_mobilenet_technical_0.11.hdf5 --image-source $(pwd)/src/tests/test_images/images/'
	#cmd=['echo','hello']
	#command = 'sudo '
	#print(command)
	
	print('Password E')
	os.system('2365')
	result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	os.system('2365')
	os.chdir(toPath)
	os.system('rm images -r')
	print('---------------')
	print(result.stdout)
	return result.stdout
	#print(output.read())
	# pscp -r your/local/directory/ userID@hostserver:/your/destination/directory
	#make connection
	#upload directory
	#copy abspath
	#use path in docker command

# @app.route('/upload/<filename>')
# def send_image(filename):
#     return send_from_directory("images", filename)
#
#
# @app.route('/gallery')
# def get_gallery():
#     image_names = os.listdir('./images')
#     print(image_names)
#     return render_template("gallery.html", image_names=image_names)


if __name__ == "__main__":
	app.run(port=5000, debug=True)
