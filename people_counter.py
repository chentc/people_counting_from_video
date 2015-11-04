"""
Copyright (c) Steven P. Goldsmith. All rights reserved.
Created by Steven P. Goldsmith on December 24, 2013
sgoldsmith@codeferm.com
"""

"""Histogram of Oriented Gradients ([Dalal2005]) object detector.
sys.argv[1] = source file or will default to "../../resources/walking.mp4" if no args passed.
@author: sgoldsmith
"""
# Configure logger

import logging, sys, time, cv2
import argparse

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)
        
        
logger = logging.getLogger("PeopleDetect")
logger.setLevel("INFO")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(module)s %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
# If no args passed then default to internal file
if len(sys.argv) < 2:
    url = "test_retail_1.mp4"
else:
    url = sys.argv[1]
outputFile = "testss.mp4"
print url
videoCapture = cv2.VideoCapture(url)
logger.info("OpenCV %s" % cv2.__version__)
logger.info("Input file: %s" % url)
logger.info("Output file: %s" % outputFile)
logger.info("Resolution: %dx%d" % (videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH),
                               videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
videoWriter = cv2.VideoWriter(outputFile, cv2.cv.CV_FOURCC('m', 'p', '4', 'v'), videoCapture.get(cv2.cv.CV_CAP_PROP_FPS),
                              (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))), True)
lastFrame = False
frames = 0
framesWithPeople = 0
start = time.time()
while not lastFrame:
    ret, image = videoCapture.read()
    if ret:
        foundLocations, foundWeights = hog.detectMultiScale(image, winStride=(8, 8), padding=(32, 32), scale=1.05)
        if len (foundLocations) > 0:
            framesWithPeople += 1
            i = 0
            for x, y, w, h in foundLocations:
                # Draw rectangle around fond object
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Print weight
                cv2.putText(image, "%1.2f" % foundWeights[i], (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), thickness=2, lineType=cv2.CV_AA)
                i += 1
    else:
        lastFrame = True
        
    if lastFrame != True:
        videoWriter.write(image)
    # cv2.imwrite(str(frames) + ".jpg", image)
    frames += 1
    print frames

elapse = time.time() - start
logger.info("%d frames, %d frames with people" % (frames, framesWithPeople))
logger.info("Elapse time: %4.2f seconds" % elapse)
del videoCapture
del videoWriter