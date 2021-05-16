import cv2 as cv
import numpy as np
import math

#cap = cv.VideoCapture('Resources\rail_without_carpet.avi')
cap = cv.VideoCapture(0)

#setup values
largest_contour_index = -1
ret, frame = cap.read()
frame_height = frame.shape[0]
frame_width = frame.shape[1]
half_frame_height = frame_height * 0.5
half_frame_width = frame_width * 0.5
print(str(frame_height) +  "x" + str(frame_width))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #gen hsv img and mask
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lowGray = np.array([3,40,109])
    highGray = np.array([28,94,216])
    mask = cv.inRange(hsv, lowGray, highGray)

    #Größte Kontur finden    
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    largest_contour_area = 0

    for i in range (len(contours)):
        if len(contours) != 0:
            moments = cv.moments(contours[i])
            area = moments['m00']

            if area > largest_contour_area:
                largest_contour_area = area
                largest_contour_index = i
                largest_moment = cv.moments(contours[largest_contour_index])
        
    #Kreis im Mittelpunkt der größten Kontur zeichnen
    if  largest_moment["m00"] != 0:
        cX1 = int(largest_moment["m10"] / largest_moment["m00"])
        cY1 = int(largest_moment["m01"] / largest_moment["m00"])
        cv.circle(frame, (cX1, cY1), 5, (255, 255, 255), -1)
    
    cv.drawContours(frame, contours, largest_contour_index, (0,255,0), 3)
    cv.line(frame, pt1=(cX1,cY1), pt2=(320,frame_height), color=(0,0,255), thickness=5)
    
    #minAreaRect, optional
    #rect = cv.minAreaRect(contours[largest_contour_index])
    #box = cv.boxPoints(rect) 
    #ox = np.int0(box)
    #cv.drawContours(frame,[box],0,(0,0,255),2)
    
    #angle calculation
    if cX1 != 176:
        m = (640-cY1)/(176-cX1)
        degree = abs(math.degrees(math.atan(m)))
        
    #speed calculation
        motor_pwm = 1.68 * degree     #Max Geschwindigkeit liegt bei PWM = 150
        print(str(degree) + (" ; ") + str(motor_pwm))
    
    

    # Display the resulting frame
    cv.imshow('binary', mask)
    cv.imshow('hsv', hsv)
    cv.imshow('original',frame)

    #stop when q pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
    

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()