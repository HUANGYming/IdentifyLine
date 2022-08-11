""" detect curves on the simulated human leg 

Usage:

    use computer camera

 """
from copy import copy
import numpy as np
import cv2
import time



class linedetector:
    def __init__(self):

        self.lines = []
 
    def find_lines(self, frame):

        # set HSV interval of black
        lower_legcolor=np.array([5,25,150])
        upper_legcolor=np.array([170,166,255])

        # change to hsv model
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        frame2 = copy(frame)
        # select black pixel and generate binary image
        binary = cv2.inRange(hsv, lower_legcolor, upper_legcolor)

        # find contours
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # find the largest contours
        temp = 0
        index = 0
        for i in range(len(contours)-1):
            Area = cv2.contourArea(contours[i])
            if Area > temp:
                temp = Area
                index = i

        mask = cv2.drawContours(frame2, contours, index, (0,255,255), 1)
        cv2.namedWindow("Largest Contours", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Largest Contours', 800,1100)
        cv2.imshow("Largest Contours", mask)

        # find the largest son-contour
        temp = 0
        largest_son_index = 0
        hierarchy = np.squeeze(hierarchy)
        if hierarchy[index][2] != -1:
            son_index = hierarchy[index][2]
            temp = cv2.contourArea(contours[son_index])
            while (hierarchy[son_index][0] != -1):
                son_index = hierarchy[son_index][0]
                Area = cv2.contourArea(contours[son_index])
                if Area > temp:
                    temp = Area
                    largest_son_index = son_index
                
            Pic_Line = cv2.drawContours(frame, contours, largest_son_index, (0,255,0), cv2.FILLED)
            cv2.namedWindow("Line", cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Line', 800,1100)
            cv2.imshow("Line", Pic_Line)

        # fit the line
        target = np.squeeze(contours[largest_son_index])

        xpts = [y for (x,y) in target]
        h, w = binary.shape      
        xpts = [(h-x) for x in xpts]

        ypts = [x for (x,y) in target]
        # curve fitting (5th power polynomial)
        coeffi = 0
        try:
            coeffi = np.polyfit(ypts, xpts, 4)
        except:
            pass
        p1 = np.poly1d(coeffi)
        xvals = p1(ypts)
        
        xvals = list(xvals)
        for i in range(len(xvals)):
            xvals[i] = int(xvals[i])
        h, w = binary.shape

        # show fit curve to original image
        xvals = [(h-x) for x in xvals]
        for point in zip(ypts, xvals):
            cv2.circle(frame, point, 2, (255,0,0), 2)
        cv2.namedWindow("image_result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image_result', 800,1100)
        cv2.imshow("image_result", frame)


        # opencv(x,y) to common coordinate(y,h-x)
        coordinate_opencv = [(x,y) for x in ypts for y in xvals]
        return coordinate_opencv, frame
 
if __name__ == "__main__":
    # open camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # start to detect and label the black curves 
        ld = linedetector()
        coordinate_opencv, frame = ld.find_lines(frame)
        key = cv2.waitKey(100)
        # press 'q' to quit
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = "out_files"+"{}.png".format(time.time())
            cv2.imwrite(filename, frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

