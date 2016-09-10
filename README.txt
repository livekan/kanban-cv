README:

This is the object detection and tracking suite for LiveKan.

This suite will run on the project managers machine, which will have a webcam watching the physical Kanban board.  When the physical Kanban board  is modified, the project managers machine will POST to the webserver so that all team members can track the updates.

Note that the project manager is still able to log in and use the analytics and other features from other machines.

This suite tracks image changes to the Kanban board and POSTs them to the server as a Json containing information on the current headers of the board and the current stickies.

This will be a JSON object in the following format:

{
	"headersArray":[column1, column2Name, ..., columnNName]
	"stickiesArray:[(Sticky1Idx, Sticky1Color, Sticky1Header), ..., (StickyNIdx, StickyNColor, StickyNHeader)]
}

The web server will also be able to make the following requests:
	Get the image data of a posty with a specific idx
	Get the current board image
	Get the image data of a specific header





	


