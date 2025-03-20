import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import os
import cv2
import constants
from gui_utils import get_filenames, hex_to_bgr
from makeup_applicator import MakeupApplicator
from model import Model


class MakeoverStudioGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Makeover Studio")
        self.root.geometry("800x800")
        self.filenames = get_filenames()

        self.model = None  # Store the original model object
        self.model_img = None  # Store the original model image
        self.original_img = None  # Store a copy of the original image for resetting
        self.current_image_file = None  # Store the file path of the current image
        self.applicator = None
        self.current_image = None

        self.image_label = None
        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):
        # Left side: Thumbnails and scrollable area
        thumbnail_frame = tk.Frame(self.root)
        thumbnail_frame.grid(row=1, column=0, padx=10, pady=10)

        # Label for thumbnails
        label = tk.Label(self.root, text=constants.CHOOSE_MODEL)
        label.grid(row=0, column=0, padx=5, pady=5)

        canvas = tk.Canvas(thumbnail_frame, width=200, height=400)
        canvas.grid(row=1, column=0)

        scrollbar = tk.Scrollbar(thumbnail_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        canvas.config(yscrollcommand=scrollbar.set)

        # Scrollable container for thumbnails
        thumbnail_canvas_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=thumbnail_canvas_frame, anchor="nw")

        # Add model image thumbnails as buttons
        for i, filename in enumerate(self.filenames):
            img = Image.open(f"{constants.MODELS_PATH}/{filename}")
            img.thumbnail((100, 100))  # Resize the image to a thumbnail size
            img_tk = ImageTk.PhotoImage(img)
            thumbnail_button = tk.Button(thumbnail_canvas_frame, image=img_tk,
                                         command=lambda i=i: self.display_image(i))
            thumbnail_button.image = img_tk  # Keep reference to the image
            thumbnail_button.grid(row=i // 2, column=i % 2, padx=5, pady=5)

        # Update scrollable region for thumbnail buttons
        thumbnail_canvas_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Right side: Display selected model image
        display_frame = tk.Frame(self.root)
        display_frame.grid(row=1, column=1, padx=10, pady=10)

        self.image_label = tk.Label(display_frame)
        self.image_label.pack()
        self.create_action_buttons()

    def create_action_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=1, columnspan=2, pady=10)

        upper_eyeliner_color_button = tk.Button(button_frame, text=constants.UPPER_EYELINER_COLOR,
                                                command=self.apply_upper_eyeliner_color)
        upper_eyeliner_color_button.grid(row=0, column=0, padx=5)

        upper_eyeliner_button = tk.Button(button_frame, text=constants.UPPER_EYELINER,
                                          command=self.apply_upper_eyeliner)
        upper_eyeliner_button.grid(row=0, column=1, padx=5)

        lower_eyeliner_color_button = tk.Button(button_frame, text=constants.LOWER_EYELINER_COLOR,
                                                command=self.apply_lower_eyeliner_color)
        lower_eyeliner_color_button.grid(row=1, column=0, padx=5)

        lower_eyeliner_button = tk.Button(button_frame, text=constants.LOWER_EYELINER,
                                          command=self.apply_lower_eyeliner)
        lower_eyeliner_button.grid(row=1, column=1, padx=5)

        lip_liner_color_button = tk.Button(button_frame, text=constants.LIP_LINER_COLOR,
                                           command=self.apply_lip_liner_color)
        lip_liner_color_button.grid(row=2, column=0, padx=5)

        lip_liner_button = tk.Button(button_frame, text=constants.LIP_LINER, command=self.apply_lip_liner)
        lip_liner_button.grid(row=2, column=1, padx=5)

        lipstick_color_button = tk.Button(button_frame, text=constants.LIPSTICK_COLOR,
                                          command=self.apply_lipstick_color)
        lipstick_color_button.grid(row=3, column=0, padx=5)

        lipstick_button = tk.Button(button_frame, text=constants.LIPSTICK, command=self.apply_lipstick)
        lipstick_button.grid(row=3, column=1, padx=5)

        reset_button = tk.Button(button_frame, text=constants.RESET, command=self.reset_image)
        reset_button.grid(row=4, column=0, columnspan=2, pady=10)

        save_image_button = tk.Button(button_frame, text=constants.SAVE_IMAGE, command=self.save_image)
        save_image_button.grid(row=4, column=1, columnspan=2, pady=10)

        exit_button = tk.Button(button_frame, text=constants.EXIT, command=self.root.quit)
        exit_button.grid(row=4, column=2, columnspan=2, pady=5)

    def display_image(self, index):
        self.current_image_file = os.path.join(constants.MODELS_PATH, self.filenames[index])
        self.model = Model(self.current_image_file)
        self.applicator = MakeupApplicator(self.model)

        self.model_img = self.model.get_opencv_image()
        self.original_img = self.model_img.copy()  # Store the original image for reset

        pil_image = Image.fromarray(cv2.cvtColor(self.model_img, cv2.COLOR_BGR2RGB))
        img_data = ImageTk.PhotoImage(pil_image)
        self.current_image = pil_image

        self.image_label.config(image=img_data)
        self.image_label.image = img_data

    def apply_upper_eyeliner_color(self):
        color = colorchooser.askcolor()[1]
        self.applicator.set_upper_eyeliner_color(hex_to_bgr(color))

    def apply_upper_eyeliner(self):
        if self.model_img is not None:
            model_with_upper_liner = self.applicator.apply_upper_eyeliner()
            pil_image = Image.fromarray(cv2.cvtColor(model_with_upper_liner, cv2.COLOR_BGR2RGB))
            img_data = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=img_data)
            self.image_label.image = img_data
            self.current_image = pil_image  # Store updated image

    def apply_lower_eyeliner_color(self):
        color = colorchooser.askcolor()[1]
        self.applicator.set_lower_eyeliner_color(hex_to_bgr(color))

    def apply_lower_eyeliner(self):
        if self.model_img is not None:
            model_with_lower_liner = self.applicator.apply_lower_liner()
            pil_image = Image.fromarray(cv2.cvtColor(model_with_lower_liner, cv2.COLOR_BGR2RGB))
            img_data = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=img_data)
            self.image_label.image = img_data
            self.current_image = pil_image  # Store updated image

    def apply_lip_liner_color(self):
        color = colorchooser.askcolor()[1]
        self.applicator.set_lip_liner_color(hex_to_bgr(color))

    def apply_lip_liner(self):
        if self.model_img is not None:
            model_with_lip_liner = self.applicator.apply_lip_liner()
            pil_image = Image.fromarray(cv2.cvtColor(model_with_lip_liner, cv2.COLOR_BGR2RGB))
            img_data = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=img_data)
            self.image_label.image = img_data
            self.current_image = pil_image  # Store updated image

    def apply_lipstick_color(self):
        color = colorchooser.askcolor()[1]
        self.applicator.set_lipstick_color(hex_to_bgr(color))

    def apply_lipstick(self):
        if self.model_img is not None:
            model_with_lipstick = self.applicator.apply_lipstick()
            pil_image = Image.fromarray(cv2.cvtColor(model_with_lipstick, cv2.COLOR_BGR2RGB))
            img_data = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=img_data)
            self.image_label.image = img_data
            self.current_image = pil_image  # Store updated image

    def reset_image(self):
        if self.original_img is not None:
            self.model_img = self.original_img.copy()  # Reset to the original image
            pil_image = Image.fromarray(cv2.cvtColor(self.model_img, cv2.COLOR_BGR2RGB))
            img_data = ImageTk.PhotoImage(pil_image)

            self.model = Model(self.current_image_file)  # Reset model object
            self.applicator = MakeupApplicator(self.model)
            self.image_label.config(image=img_data)
            self.image_label.image = img_data

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                     ("JPEG files", "*.jpg;*.jpeg"),
                                                                                     ("All files", "*.*")])
        if file_path:
            self.current_image.save(file_path)
