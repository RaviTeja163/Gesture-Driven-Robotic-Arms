import unittest
import cv2
import mediapipe as mp
from robodk import robolink

from move import recognize_hands

class TestRobotControl(unittest.TestCase):

    def test_recognize_hands_single_hand(self):
        # Test case for recognizing hand gestures with a single hand
        # Assuming 1 finger extended
        x_coord = [100, 150, 200, 250, 300]
        y_coord = [200, 180, 160, 140, 120]
        result = recognize_hands(x_coord, y_coord)
        self.assertEqual(result, [0, 1, 0, 0, 0])

    def test_recognize_hands_multiple_fingers(self):
        # Test case for recognizing hand gestures with multiple fingers extended
        # Assuming 2 fingers extended
        x_coord = [100, 150, 200, 250, 300]
        y_coord = [200, 180, 160, 140, 120]
        result = recognize_hands(x_coord, y_coord)
        self.assertEqual(result, [0, 1, 1, 0, 0])

    def test_recognize_hands_left_hand(self):
        # Test case for recognizing hand gestures with a left hand
        # Assuming 3 fingers extended
        x_coord = [100, 150, 200, 250, 300]
        y_coord = [200, 180, 160, 140, 120]
        result = recognize_hands(x_coord, y_coord)
        self.assertEqual(result, [0, 1, 1, 1, 0])

if __name__ == '__main__':
    unittest.main()
