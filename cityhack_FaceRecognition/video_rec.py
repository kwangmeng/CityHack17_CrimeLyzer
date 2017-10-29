from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as  plt
import numpy as np
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

#J Import function for saving to SQL
#import mysql.connector

#J Dabase Credentials (Still need to edit)
#db = mysql.connector.connect(user='root', password='abhi',
#                              host='localhost',
#                              database='cbir')

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
dbimagepath = sys.argv[2]


jason = cv2.imread(dbimagepath)


# Initiate the log file
log.basicConfig(filename='webcam.log',level=log.INFO)

# Use webcam to record video
video_capture = cv2.VideoCapture(0)
anterior = 0

#COmpareface.py we copied feelsbad
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB,multichannel=True)

	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")

	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")

	# show the images
	plt.show()
#no longer feelsbad

while True:

    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    
    )


    #J Getting image to compare_images
    jason = cv2.imread(dbimagepath)

    jason = cv2.resize(jason, (300, 300))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #J Crop into individual faces but in video form
        roi = frame[y:y+h, x:x+w]
        #cv2.imshow("FacesDectected",roi)
        fakeroi = cv2.resize(roi, (300, 300))
        compare_images(fakeroi,jason,"bobo")

    # Saving number of face detected into log file
    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    #J Save the image into dabase

    #J Compare with db


    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
