from cv2 import cv2 as cv
import numpy as np
import math

cap = cv.VideoCapture('Resources/rail2.avi')
#cap = cv.VideoCapture(0)
largest_contour_index = -1

ret, frame = cap.read()
frame_height = frame.shape[0]
frame_width = frame.shape[1]
half_frame_height = frame_height * 0.5
half_frame_width = frame_width * 0.5
print(str(frame_height) +  "x" + str(frame_width))

mask_line_mat = np.zeros((frame_height, frame_width), dtype=np.uint8)
mask_trafficlight = np.zeros((frame_height,frame_width,3), dtype=np.uint8)

rect_line = cv.rectangle(mask_line_mat,(0,180),(frame_width,frame_height), (255,255,255), cv.FILLED)
rect_trafficlight = cv.rectangle(mask_trafficlight,(423,0),(frame_width,frame_height),(255,255,255),cv.FILLED)

print(str(mask_line_mat))
print(str(mask_trafficlight.shape))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # frame to gray and binary image
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_inv = cv.bitwise_not(gray)
    ret, binary = cv.threshold(gray_inv,150,170,cv.THRESH_BINARY)
    
    #frame to hsv and creating a green mask
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_green = np.array([35, 140, 60]) 
    upper_green = np.array([255, 255, 180])
    mask_trafficlight = cv.inRange(hsv_frame, lower_green, upper_green) 
 
    #mask erstellen
    mask_line_binary = cv.bitwise_and(mask_line_mat, binary)
    #mask_trafficlight_color = cv.bitwise_and(mask_trafficlight, hsv_frame)

    contours, hierarchy = cv.findContours(mask_line_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    largest_contour_area = 0

    #Größte Kontur finden
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
    
    #Berechnung des Winkels der Schienen zur Kamera
    if cX1 != 176:
        m = (640-cY1)/(176-cX1)
        degree = abs(math.degrees(math.atan(m)))
        
        #Berechung der Motoransteuerung
        motor_pwm = 1.68 * degree     #Max Geschwindigkeit liegt bei PWM = 150
        print(str(degree) + (" ; ") + str(motor_pwm))
    
    

    # Display the resulting frame
    cv.imshow('binary', binary)
    cv.imshow('mask_line binary', mask_line_binary)
    cv.imshow('original',frame)
    cv.imshow('mask_trafficlight',mask_trafficlight)

    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
    

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()