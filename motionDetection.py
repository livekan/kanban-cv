import numpy as np
import cv2

import time
starttime=time.time()


cap = cv2.VideoCapture(1)

fgbg = cv2.BackgroundSubtractorMOG()



counter=0


def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)


while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame, learningRate=0.001)
    if (counter==0):
	#firstBoard=KanbanBoard(frame)
	darkness=fgmask

    cv2.imshow('frame',fgmask)

    k = cv2.waitKey(30) & 0xff
    threshold=np.sum(diffImg(darkness, fgmask, darkness))
    counter+=1
    if (threshold<3000 and counter>=0): 
	#board= KanbanBoard(frame)
	if True: #!(firstBoard.sameBoard(secondBoard)):
		print "this is where we post firstBoard.data"
	else:
		continue;
	
    time.sleep(0.25 - ((time.time() - starttime) % 0.25))


cap.release()
cv2.destroyAllWindows()


