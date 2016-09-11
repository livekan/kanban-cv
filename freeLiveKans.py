# USAGE
# python detect_color.py --image example_shapes.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2
import numpy as np
import time
import json
import uuid
import urllib2
import urllib
import base64
import getopt
import MultipartPostHandler
import os
import re
import sys
from AbbyyOnlineSdk import *
import skfuzzy
import hmmlearn

starttime=time.time()

cap = cv2.VideoCapture(0)

fgbg = cv2.BackgroundSubtractorMOG()



counter=0
threshold=0




processor = AbbyyOnlineSdk()

if "ABBYY_APPID" in os.environ:
	processor.ApplicationId = os.environ["ABBYY_APPID"]

if "ABBYY_PWD" in os.environ:
	processor.Password = os.environ["ABBYY_PWD"]

# Proxy settings
if "http_proxy" in os.environ:
	proxyString = os.environ["http_proxy"]
	print "Using proxy at %s" % proxyString
	processor.Proxy = urllib2.ProxyHandler( { "http" : proxyString })



# Recognize a file at filePath and save result to resultFilePath
def recognizeFile( filePath, resultFilePath, language, outputFormat ):
	print "Uploading.."
	settings = ProcessingSettings()
	settings.Language = language
	settings.OutputFormat = outputFormat
	task = processor.ProcessImage( filePath, settings )
	if task == None:
		print "Error"
		return
	print "Id = %s" % task.Id
	print "Status = %s" % task.Status

	# Wait for the task to be completed
	sys.stdout.write( "Waiting.." )
	# Note: it's recommended that your application waits at least 2 seconds
	# before making the first getTaskStatus request and also between such requests
	# for the same task. Making requests more often will not improve your
	# application performance.
	# Note: if your application queues several files and waits for them
	# it's recommended that you use listFinishedTasks instead (which is described
	# at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

	while task.IsActive() == True :
		time.sleep( 5 )
		sys.stdout.write( "." )
		task = processor.GetTaskStatus( task )

	print "Status = %s" % task.Status
	
	if task.Status == "Completed":
		if task.DownloadUrl != None:
			processor.DownloadResult( task, resultFilePath )
			print "Result was written to %s" % resultFilePath
	else:
		print "Error processing task"


class Sticky(object):
	def __init__(self, color, shape, isHeader, data, midpoint):
		self.color = color
		self.idx =  uuid.uuid4().int 
		self.isHeader = isHeader
		self.data = data
		self.area = cv2.contourArea(data)
		self.shape = shape
		self.midpoint = midpoint
		self.parentHeader= None
		self.text=""
	def setHeader(self, header):
		self.parentHeader= header
	def imageDif(self, otherSticky): return True
	def metadata(self):
		return {"asignee": "", "text": str(text), "color": str(self.color), "desc": ""}

	def compare(self, otherSticky):
		if (self.midpoint != otherSticky.midpoint): return False
		if (self.color != otherSticky.color) : return False
		if (self.parentHeader != otherSticky.parentHeader) : return False

		return (self.setHeader(otherSticky))


stickies  = []
headers = []

counter=0




def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)


def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0
  

while(1):
	ret, frame = cap.read()

	fgmask = fgbg.apply(frame, learningRate=0.10)
	image=frame
	if (counter==0):
		firstFrame=frame
		darkness=fgmask

	if (threshold<10000 and counter>=0): 
		resized = imutils.resize(image, width=300)
		image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(resized, (5, 5), 0)
		image=cv2.equalizeHist(image)

		# load the image and resize it to a smaller factor so that
		# the shapes can be approximated better

		ratio = image.shape[0] / float(resized.shape[0])

		# blur the resized image slightly, then convert it to both
		# grayscale and the L*a*b* color spaces

		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
		cv2.imshow("Thresh", thresh)

		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# initialize the shape detector and color labeler
		sd = ShapeDetector()
		cl = ColorLabeler()

		building=[]
		for each in cnts:
			area=(cv2.contourArea(each))
			if ((area > 500.0) or (area < 2000.0)):  building.append(each)

		cnts=building


		# loop over the contours
		for c in cnts:
			# compute the center of the contour
			M = cv2.moments(c)
			if (M["m00"] !=0.0):
				cX = int((M["m10"] / M["m00"]) * ratio)
				cY = int((M["m01"] / M["m00"]) * ratio)

				# detect the shape of the contour and label the color
				shape = sd.detect(c)
				color = cl.label(lab, c)
	
				# multiply the contour (x, y)-coordinates by the resize ratio,
				# then draw the contours and the name of the shape and labeled
				# color on the image
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				text = "{} {}".format(color, shape)
				cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
				cv2.putText(image, text, (cX, cY),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
				newSticky= Sticky(str(color), str(shape), -1, c, (cX, cY))

				x, y, width, height = cv2.boundingRect(c)
				roi = frame[y:y+height, x:x+width]
				cv2.imwrite("roi.png", roi)
				recognizeFile( "roi.png", "out.txt", 'English', 'txt')
				with open("out.txt", "r") as f:
					newSticky.text=f.read().replace('\n', '')
				stickies.append(newSticky)



		#find the headers of this image	
		areas=[]	
		for each in stickies:
			areas.append(each.area)
		medianA=median(areas)
		for each in stickies:
			if each.area>(medianA*8): stickies.remove(each)
			elif each.area>(medianA*1.75):
				headers.append(each)

			each.setHeader(each.idx)
			each.isHeader=1

		#clustering algorithms

		numHeaders=  len(headers)
		xpts=[each.midpoint[0] for each in stickies]
		ypts=[each.midpoint[1] for each in stickies]
		alldata = np.vstack((xpts, ypts))

		cntr, u_orig, _, _, _, _, _ = skfuzzy.cluster.cmeans(alldata, numHeaders, 2, error=0.08, maxiter=1000)
		print "Clustering"
		print "Number of clusters " + str((numHeaders))
		#	print "Areas are " + str(areas)
		#	print "Stickies are "+ str(stickies)
		#	print "Clusters are " + str(cntr)
		centerRep=[]	
		for j in range(numHeaders):
			centerRep.append((alldata[0, u_orig.argmax(axis=0) == j], alldata[1, u_orig.argmax(axis=0) == j]))
		contourBuckets=[]
		stickyBuckets=[]
		for i in xrange(numHeaders): 
			contourBuckets.append([])
			stickyBuckets.append([])
		#	print contourBuckets	
		#	print "cntr" + str(cntr)
		#	print "numHeaders" + str(numHeaders)
		#	print "centerRep" + str(centerRep)
		for i in xrange(len(centerRep)):
			for t in xrange(len(centerRep[i][0])):
		#			print "center i is " + str(centerRep[i])
		#			print "centerRep" + str(centerRep)
		#			print str(i)+ "and" + str(t)
				x=centerRep[i][0][t]
				y=centerRep[i][1][t]		
				for each in stickies:
					if each.midpoint== (x,y): 
						stickyBuckets[i].append(each)
						contourBuckets[i].append(each.data)

		#	print "contour buckets is" + str(contourBuckets)
		#populate headers:
		for stickyBucketN in stickyBuckets:
			foundHeader=None				
			for each in stickyBucketN:
				if (each.parentHeader != None):
					#could handle this case if there already was a parent header in cluster			
					foundHeader = each.parentHeader
					break
				else: each.isHeader=0
			for each in stickyBucketN:				
				each.setHeader(foundHeader)
		
		#output to json
		outputJson=[]
		for val in stickyBuckets:
			currentList=[]
			for each in val:		
				currentList.append(each.metadata())
			outputJson.append(currentList)

		outputJson= json.dumps(outputJson)
		#req = urllib2.Request("http://de66c8cc.ngrok.io/api/kanban")
		#req.add_header('Content-Type', 'application/json')

		print outputJson
		response = urllib2.urlopen(req, outputJson)
	



		image2=frame

		for i in xrange(len(contourBuckets)):
			x=(i*255/len(contourBuckets))
			y=(i*255/len(contourBuckets))
			z=(i*255/len(contourBuckets))
		#	print contourBuckets[i]
			cv2.drawContours(image2, contourBuckets[i], -1, (0,0,z) , 2)
		cv2.imshow("testing",image2)

		#print "\n\n"

		# show the output image
		cv2.imshow('doesntMatter',image)
		headers=[]
		stickies=[]

		counter=0
		k = cv2.waitKey(30) & 0xff
	
	threshold=np.sum(diffImg(darkness, fgmask, darkness))
	print threshold
	counter+=1

	
	#board= KanbanBoard(frame)

	if True: #!(firstBoard.sameBoard(secondBoard)):
		print "this is where we post firstBoard.data"
	else:
		continue;

	time.sleep(0.25 - ((time.time() - starttime) % 0.25))


cap.release()
cv2.destroyAllWindows()



