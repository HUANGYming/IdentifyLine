""" detect black curves (must no interference)

Typical usage example:
    
    identify a black line on white table
    
Usage:

    use computer camera

 """

import numpy as np
import cv2

# detect black curves and label them on the original image
class linedetector:
    def __init__(self):

        self.lines = []
 
    def find_lines(self, frame):

        # set HSV interval of black
        lower_black=np.array([0,0,0])
        upper_black=np.array([180,255,46])

        # change to hsv model
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # select black pixel and generate binary image
        binary = cv2.inRange(hsv, lower_black, upper_black)
        cv2.namedWindow("binary image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('binary image', 800,1100)
        cv2.imshow("binary image", binary)

        # downsample the image to increase running speed 
        downSampled = cv2.pyrDown(binary)
        dist = downSampled
        cv2.namedWindow("downSampled image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('downSampled image', 800,1100)
        cv2.imshow("downSampled image", dist)

        # transform the black pixel to corresponding x and y coordinates
        h, w = dist.shape
        threshold_d = 100
        result = np.zeros((h, w), dtype=np.uint8)
        xpts = []
        ypts = []
        for row in range(h):
            for col in range(w):
                d = dist[row][col]
                if d > threshold_d:
                    xpts.append(h-row)
                    ypts.append(col)
                    result[row][col] = 255

        # curve fitting (5th power polynomial)
        coeffi = np.polyfit(ypts, xpts, 5)
        p1 = np.poly1d(coeffi)
        xvals = p1(ypts)
        xvals = list(xvals)
        for i in range(len(xvals)):
            xvals[i] = int(xvals[i])
        
        # Coordinateds converted to opencv format
        for i in range(len(xvals)):
            xvals[i] = h - xvals[i]

        # show fit curve to original image
        downSampled_frame = cv2.pyrDown(frame)
        for point in zip(ypts, xvals):
            cv2.circle(downSampled_frame, point, 2, (0,0,255), 2)
        cv2.namedWindow("image_result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image_result', 800,1100)
        cv2.imshow("image_result", downSampled_frame)

        return 0


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
        lines = ld.find_lines(frame)

        # press 'q' to quit
        if cv2.waitKey(100) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
