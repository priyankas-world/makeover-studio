import constants
import cv2
import numpy as np
from scipy.interpolate import CubicSpline


class MakeupApplicator:

    def __init__(self, model):
        self.makeover_model = model
        self.image = self.makeover_model.get_opencv_image()
        self.coordinates = self.makeover_model.get_facial_coords()
        self.upper_eyeliner_color = (0, 0, 0)  # Default color = black
        self.lower_eyeliner_color = (0, 0, 0)  # Default color = black
        self.lipstick_color = (25, 0, 150)  # Default color = muted magenta
        self.lip_liner_color = (25, 0, 150)  # Default color = muted magenta

    def apply_upper_eyeliner(self):
        upper_eye_l = self.coordinates[constants.EYE_L_OUTER:constants.EYE_L_INNER]
        upper_eye_r = self.coordinates[constants.EYE_R_INNER:constants.EYE_R_OUTER]
        print(len(self.coordinates[0]))
        l_x = upper_eye_l[:, 0]
        l_y = upper_eye_l[:, 1]
        r_x = upper_eye_r[:, 0]
        r_y = upper_eye_r[:, 1]

        approximated_curve_l = CubicSpline(l_x, l_y)
        approximated_curve_r = CubicSpline(r_x, r_y)

        l_x_new = np.linspace(min(l_x), max(l_x), 100)
        l_y_new = approximated_curve_l(l_x_new)

        r_x_new = np.linspace(min(r_x), max(r_x), 100)
        r_y_new = approximated_curve_r(r_x_new)

        l_curve_points = np.vstack((l_x_new, l_y_new)).T.astype(np.int32).reshape((-1, 1, 2))
        r_curve_points = np.vstack((r_x_new, r_y_new)).T.astype(np.int32).reshape((-1, 1, 2))

        cv2.polylines(img=self.image, pts=[l_curve_points], isClosed=False, color=self.upper_eyeliner_color,
                      thickness=2)
        cv2.polylines(img=self.image, pts=[r_curve_points], isClosed=False, color=self.upper_eyeliner_color,
                      thickness=2)
        return self.image

    def apply_lower_liner(self):
        lower_eye_l = self.coordinates[constants.EYE_L_INNER_START:constants.EYE_L_LOWER]
        lower_eye_l = np.vstack((self.coordinates[constants.EYE_L_OUTER], lower_eye_l))
        lower_eye_r = self.coordinates[constants.EYE_R_OUTER_START:constants.EYE_R_LOWER]
        lower_eye_r = np.vstack((self.coordinates[constants.EYE_R_INNER], lower_eye_r))

        # Sort arrays in order based on x coordinate (left to right)
        lower_eye_l = lower_eye_l[tuple([np.argsort(lower_eye_l[:, 0])])]
        lower_eye_r = lower_eye_r[tuple([np.argsort(lower_eye_r[:, 0])])]

        # Get individual x and y arrays for each eye
        l_x = lower_eye_l[:, 0]
        l_y = lower_eye_l[:, 1]
        r_x = lower_eye_r[:, 0]
        r_y = lower_eye_r[:, 1]

        # Approximate the curves of each lower lash line and add new points
        approximated_curve_l = CubicSpline(l_x, l_y)
        approximated_curve_r = CubicSpline(r_x, r_y)

        l_x_new = np.linspace(min(l_x), max(l_x), 100)
        l_y_new = approximated_curve_l(l_x_new)

        r_x_new = np.linspace(min(r_x), max(r_x), 100)
        r_y_new = approximated_curve_r(r_x_new)

        l_curve_points = np.vstack((l_x_new, l_y_new)).T.astype(np.int32).reshape((-1, 1, 2))
        r_curve_points = np.vstack((r_x_new, r_y_new)).T.astype(np.int32).reshape((-1, 1, 2))

        # Make transparent
        overlay = self.image.copy()
        cv2.polylines(img=overlay, pts=[l_curve_points], isClosed=False, color=self.lower_eyeliner_color, thickness=2)
        cv2.polylines(img=overlay, pts=[r_curve_points], isClosed=False, color=self.lower_eyeliner_color, thickness=2)
        cv2.addWeighted(overlay, 0.5, self.image, 1 - 0.5, 0, self.image)
        return self.image

    def apply_lipstick(self):
        lip_outer = self.coordinates[constants.LIPS_OUTER_START:constants.LIPS_OUTER_END].reshape((-1, 1, 2))
        # Make transparent
        overlay = self.image.copy()
        cv2.fillPoly(img=overlay, pts=[lip_outer], color=self.lipstick_color)
        cv2.addWeighted(overlay, 0.5, self.image, 1 - 0.5, 0, self.image)
        return self.image

    def apply_lip_liner(self):
        lip_outer = self.coordinates[constants.LIPS_OUTER_START:constants.LIPS_OUTER_END].reshape((-1, 1, 2))

        # Make transparent
        overlay = self.image.copy()
        cv2.polylines(img=overlay, pts=[lip_outer], isClosed=True, color=self.lip_liner_color,
                      thickness=2)
        cv2.addWeighted(overlay, 0.5, self.image, 1 - 0.5, 0, self.image)
        return self.image

    def set_lipstick_color(self, new_color):
        self.lipstick_color = new_color

    def set_upper_eyeliner_color(self, new_color):
        self.upper_eyeliner_color = new_color

    def set_lower_eyeliner_color(self, new_color):
        self.lower_eyeliner_color = new_color

    def set_lip_liner_color(self, new_color):
        self.lip_liner_color = new_color
