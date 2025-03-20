import os

import cv2

import constants


def hex_to_bgr(color):
    color = color.lstrip('#')
    return tuple(int(color[i:i + 2], 16) for i in (4, 2, 0))


def get_filenames():
    filenames = []
    for file_name in os.listdir(constants.MODELS_PATH):
        file_path = os.path.join(constants.MODELS_PATH, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            img = cv2.imread(file_path)
            if img is not None:
                filenames.append(file_name)
    return filenames
