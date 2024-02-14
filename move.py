
import cv2 as cv
import mediapipe as mp
from robodk import robolink    # RoboDK API

RDK = robolink.Robolink()

white = RDK.Item('ABB IRB 1100-4/0.58')
orange = RDK.Item('ABB IRB 140-6/0.8')
target1l = RDK.Item('W1')
target2l = RDK.Item('W2')
target3l = RDK.Item('W3')
target4l = RDK.Item('W4')
target5l = RDK.Item('W5')
target1r = RDK.Item('O1')
target2r = RDK.Item('O2')
target3r = RDK.Item('O3')
target4r = RDK.Item('O4')
target5r = RDK.Item('O5')

finger_tips = [8, 12, 16, 20]
vid = cv.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

def recognize_hands(x_coord, y_coord):
	num_arr = []
	if abs(x_coord[13]-x_coord[4]) > 50:
		num_arr.append(1)
	else:
		num_arr.append(0)
	for f in finger_tips:
		if y_coord[f] < y_coord[f-2]:
			num_arr.append(1)
		else:
			num_arr.append(0)
	return num_arr

while True:
	_, img = vid.read()
	img = cv.flip(img, 1)
	h, w, d = img.shape
	result = hands.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))

	if result.multi_hand_landmarks:
		rx_coord = []
		ry_coord = []
		lx_coord = []
		ly_coord = []
		
		if len(result.multi_hand_landmarks) == 1:
			landmarks = result.multi_hand_landmarks[0]
			if (result.multi_handedness[0].classification[0].label == 'Right') and (result.multi_handedness[0].classification[0].score > 0.95):
				for l in landmarks.landmark:
					x = int(w*l.x)
					y = int(h*l.y)

					rx_coord.append(x)
					ry_coord.append(y)

			elif (result.multi_handedness[0].classification[0].label == 'Left') and (result.multi_handedness[0].classification[0].score > 0.95):
				for l in landmarks.landmark:
					x = int(w*l.x)
					y = int(h*l.y)

					lx_coord.append(x)
					ly_coord.append(y)
			
			else:
				continue

			mp_draw.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)
		
		elif len(result.multi_hand_landmarks) == 2:
			if (result.multi_handedness[0].classification[0].label == 'Left' and result.multi_handedness[0].classification[0].score > 0.95) or (result .multi_handedness[1].classification[0].label == 'Right' and result.multi_handedness[1].classification[0].score > 0.95):
				left_landmarks = result.multi_hand_landmarks[0]
				right_landmarks = result.multi_hand_landmarks[1]
			elif (result.multi_handedness[0].classification[0].label == 'Right' and result.multi_handedness[0].classification[0].score > 0.95) or (result .multi_handedness[1].classification[0].label == 'Left' and result.multi_handedness[1].classification[0].score > 0.95):
				left_landmarks = result.multi_hand_landmarks[1]
				right_landmarks = result.multi_hand_landmarks[0]
			else:
				continue

			for l in right_landmarks.landmark:
				x = int(w*l.x)
				y = int(h*l.y)

				rx_coord.append(x)
				ry_coord.append(y)

			for l in left_landmarks.landmark:
				x = int(w*l.x)
				y = int(h*l.y)

				lx_coord.append(x)
				ly_coord.append(y)

			mp_draw.draw_landmarks(img, right_landmarks, mp_hands.HAND_CONNECTIONS)
			mp_draw.draw_landmarks(img, left_landmarks, mp_hands.HAND_CONNECTIONS)

		if len(lx_coord) != 0:
			left_finger_arr = recognize_hands(lx_coord, ly_coord)

			if left_finger_arr == [0,1,0,0,0]:
				cv.putText(img, 'Left: 1', (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=1)
				white.MoveJ(target1l)
				white.RunInstruction('Program_Done')
			
			if left_finger_arr == [0,1,1,0,0]:
				cv.putText(img, 'Left: 2', (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=1)
				white.MoveJ(target2l)
				white.RunInstruction('Program_Done')
			
			if left_finger_arr == [0,1,1,1,0]:
				cv.putText(img, 'Left: 3', (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=1)
				white.MoveJ(target3l)
				white.RunInstruction('Program_Done') 

			if left_finger_arr == [0,1,1,1,1]:
				cv.putText(img, 'Left: 4', (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=1)
				white.MoveJ(target4l)
				white.RunInstruction('Program_Done') 

			if left_finger_arr == [1,1,1,1,1]:
				cv.putText(img, 'Left: 5', (50,100), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=1)
				white.MoveJ(target5l)
				white.RunInstruction('Program_Done')
				
		if len(rx_coord) != 0:
			right_finger_arr = recognize_hands(rx_coord, ry_coord)

			if right_finger_arr == [0,1,0,0,0]:
				cv.putText(img, 'Right: 1', (450,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness=1)
				orange.MoveJ(target1r)
				orange.RunInstruction('Program_Done')
			
			if right_finger_arr == [0,1,1,0,0]:
				cv.putText(img, 'Right: 2', (450,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness=1)
				orange.MoveJ(target2r)
				orange.RunInstruction('Program_Done')
			
			if right_finger_arr == [0,1,1,1,0]:
				cv.putText(img, 'Right: 3', (450,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness=1)
				orange.MoveJ(target3r)
				orange.RunInstruction('Program_Done') 

			if right_finger_arr == [0,1,1,1,1]:
				cv.putText(img, 'Right: 4', (450,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness=1)
				orange.MoveJ(target4r)
				orange.RunInstruction('Program_Done') 

			if right_finger_arr == [1,1,1,1,1]:
				cv.putText(img, 'Right: 5', (450,100), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), thickness=1)
				orange.MoveJ(target5r)
				orange.RunInstruction('Program_Done')
			
	cv.imshow('Vid',img)
	cv.waitKey(1)  

