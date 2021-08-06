#%pip install dlib						#dlib helps in finding embeddings
#%pip install face_recognition			#requires dlib, used because in 1 single line comparison can be made
#%pip install imutils

from imutils import paths
import pickle
import cv2
import os								#to interact with os
import face_recognition

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images('/content/drive/My Drive/Face Dataset'))		#storing path of all images
print(imagePaths)
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]			#-2 means 2nd last
	# load the input image and convert it from BGR (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)						#cv2 reads in bgr format
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)		#converting bgr to rgb
 	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb, model= "hog")		#detects face in rgb image using hog
	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)
	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)
  # dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("/content/drive/My Drive/encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
print("DONE")