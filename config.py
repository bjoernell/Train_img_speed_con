from cv2 import cv2 as cv
cap = cv.VideoCapture('/Users/bjornellwert/Documents/git_projects/Python/Resources/train.avi')
ret, frame = cap.read()
frame_height = frame.shape[0]
frame_width = frame.shape[1]
half_frame_height = frame_height * 0.5
half_frame_width = frame_width * 0.5
print(str(frame_height) +  "x" + str(frame_width))
