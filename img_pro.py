import cv2 as cv
import numpy as np
import math
import i2c_com
#cap = cv.VideoCapture('Resources\line.avi')
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
    #Deckenlicht:
    #lowGray = np.array([0,30,0])
    #highGray = np.array([50,140,80])
    #Tageslicht:
    lowGray = np.array([80,50,20])
    highGray = np.array([115,165,240])
    mask = cv.inRange(hsv, lowGray, highGray)

    #Groeßte Kontur finden    
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
    if len(contours) != 0:
        if  largest_moment["m00"]:
            cX1 = int(largest_moment["m10"] / largest_moment["m00"])
            cY1 = int(largest_moment["m01"] / largest_moment["m00"])
            cv.circle(frame, (cX1, cY1), 5, (255, 255, 255), -1)       
        cv.drawContours(frame, contours, largest_contour_index, (0,255,0), 3)
        cv.line(frame, pt1=(cX1,cY1), pt2=(320,frame_height), color=(0,0,255), thickness=5)
    
        #angle calculation
        if cX1 != 176:
            m = (640-cY1)/(176-cX1)
            degree = round(abs(math.degrees(math.atan(m))))
            
        #speed calculation and transmission
            motor_pwm = (0.12 * degree*degree) - (16.66 * degree) + 650     #Max Speed PWM = 50
            print(str(degree) + (" ; ") + str(motor_pwm))
            i2c_com.transmitSpeed(motor_pwm)

    # Display the resulting frame
    cv.imshow('binary', mask)
    cv.imshow('hsv', hsv)
    cv.imshow('original',frame)

    #stop when q pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
    

# When everything done, release the capture
i2c_com.transmitSpeed(0)
cap.release()
cv.destroyAllWindows()