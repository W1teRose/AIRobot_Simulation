from Controller import Controller
import numpy as np
from PIL import ImageGrab
import cv2
import threading
import struct

#stores the received control and position-matrix in a global variables
controls = "0:0:0"
posMatrixStr = "\x00"

#start the UDP connection to Unity for the controls and the position-matrix
cntControls = Controller("127.0.0.1", 5002)
cntPosMatrix = Controller("127.0.0.1", 5003)

#define function to get the controls from the Unity UDP sender 
def getControls():
	#get the controls from the unity Input.GetAxis function
	#in the format: [horizontal]:[vertical]:[height]:[graping]
	while True:
		global controls
		controls, address = cntControls.recvData()

#define function to get the position-matrix from the Unity UDP sender 
def getPosMatrix():
	#get the controls from the unity Input.GetAxis function
	#in the format: [horizontal]:[vertical]:[height]:[graping]
	while True:
		global posMatrixStr
		posMatrixStr, address = cntPosMatrix.recvData()


cntControls.startController()
cntPosMatrix.startController()
print("start Controller")

#start the getControls function in a new thread to avoid data stagnation while reading image data
threadControls = threading.Thread(target=getControls)
threadPosMatrix = threading.Thread(target=getPosMatrix)
threadControls.start()
threadPosMatrix.start()

while True:
	#print controls to console
	print(controls)
	posMatrix = struct.unpack_from("f", "\x00\x00\x00\x00\x07\x80\x00\x03")
	posMatrix = np.fromstring(posMatrixStr, dtype='float')
	#if posMatrixStr != "\x00": posMatrix = np.reshape(posMatrix, (35,35,11))
	print(posMatrix.shape)

	#read the screen, put it in to an numpy array and show it in a window
	printscreen = np.array(ImageGrab.grab(bbox=(5,45,755,545)))
	cv2.imshow('screen', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))



	if cv2.waitKey(25) & 0xFF == ord('q'): #quit statement 
            cv2.destroyAllWindows()
            break

