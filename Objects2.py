import numpy
import cv2
import uuid

class Image(object):
	def __init__(self, image):
		self.image=image
		self.squares=find_squares(image)
	def __init__(self):
		image=None
	def angle_cos(p0, p1, p2):
	    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

	def find_squares(self):
	    img=self.image
	    img = cv2.GaussianBlur(img, (5, 5), 0)
	    squares = []
	    for gray in cv2.split(img):
		for thrs in xrange(0, 255, 26):
		    if thrs == 0:
		        bin = cv2.Canny(gray, 0, 50, apertureSize=5)
		        bin = cv2.dilate(bin, None)
		    else:
		        retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
		    contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		    for cnt in contours:
		        cnt_len = cv2.arcLength(cnt, True)
		        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
		        if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
		            cnt = cnt.reshape(-1, 2)
		            max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
		            if max_cos < 0.1:
		                squares.append(cnt)
	    return squares
	def getNumberOfHeaders(self) #returns the number of headers (the number of large squares)

class Square(object):
	def getHeader(headerRanges):
		#buckets header based on mean distance between headers
		return "foo"
	def getColor(self):
		#iterates over numpy array getting rgb values, averaging and then bucketing to nearest buckets of certain colors by rounding
		return "red" 
	def getMidpointCoords(self):
		#gets the midpoint (in the horizontal dimension) of the given square--  used to break headers into columns
		return (0,0)

	def __init__(self, numpyRanges, headerRanges):
		self.color=getColor(imageStuff)
		self.idx =  UUID.int(uuid.uuid1())
		self.header = getHeader(headerRanges)
		self.numpyRanges=numpyRanges
		self.headerRanges=headerRanges

	#creates a kanban board from an image.  If called with a json we create it from the json rather than the image
	def getHeaders(self):
		#returns the current headers of the Kanban board
		return []

class LiveKan(object):
	def initStickies(self): #initializes the stickies with the given header thresholds
	def getStickiesInHeader(self, header):
		#returns the stickies in this header
	def getAllOfColor(self, color):
		#returns all stickies of a given color
	#REACH: def getStickieAuthor
	def getStickieInfo(self, stickyIdx): #returns the info of a particular sticky Idx
	def getBoard(self): #returns an array of the tuples of the stickyIdxs and their column in the board and an array of the current headers
	def compareBoards(self, otherKanbanBoard): #compares the results from getBoard(self) and getBoard(otherKanbanBoard) to make sure that the boards are the same.  Returns true or false
	def lightBoardToJson(self): #returns the board as a json representation as an array of stickies (without data) and an array of  column headers
	def getSticky(self, idx)  #must request
	def getImage(self):
	
class sticky(object):
	def __init__ (self, idx, stickyWithoutData, stickyData)

class stickyWithoutData(object):
	def  __init__(self, numPyArray, header): #inits the sticky with its color, idx, header, data(the numpy pixelArray)
	def initColor: #inits the color
	def get
	#def initHandwritingData: #inits the handwriting data by grabbing it
	def compareStickies:  #compares color, header 
	

class square(object):
	idx=0
	color=""
	numPyIdx

