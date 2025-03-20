import imutils
from imutils import face_utils
import dlib
import cv2

from constants import PREDICTOR_PATH


class Model:
    file_name = ""

    def __init__(self, file_name):
        self.file_name = file_name

    def get_opencv_image(self):
        image = cv2.imread(self.file_name)
        image = imutils.resize(image, width=500, height=500)
        return image

    def get_facial_coords(self):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(PREDICTOR_PATH)

        image = self.get_opencv_image()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)
        if len(faces) != 1:
            raise Exception('Photo must contain exactly one face')

        face = faces[0]
        shape = predictor(gray, face)
        shape_coords = face_utils.shape_to_np(shape)
        return shape_coords
