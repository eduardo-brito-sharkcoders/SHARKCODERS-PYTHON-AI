import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

class ImageEditorApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("600x600")

        # UI Elements
        self.btn_open = tk.Button(root, text="Open Image", command=self.open_image)
        self.btn_open.pack()

        # Canvas size defined
        self.canvas_width = 500
        self.canvas_height = 350
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.frame_controls = tk.Frame(root)
        self.frame_controls.pack()

        self.btn_rotate_left = tk.Button(self.frame_controls, text="<", command=self.rotate_left)
        self.btn_rotate_left.grid(row=0, column=0, padx=5, pady=5)

        self.btn_rotate_right = tk.Button(self.frame_controls, text=">", command=self.rotate_right)
        self.btn_rotate_right.grid(row=0, column=1, padx=5, pady=5)

        self.btn_grayscale = tk.Button(self.frame_controls, text="Grayscale", command=self.apply_grayscale)
        self.btn_grayscale.grid(row=0, column=2, padx=5, pady=5)

        self.btn_save = tk.Button(self.frame_controls, text="Save Image", command=self.save_image)
        self.btn_save.grid(row=0, column=3, padx=5, pady=5)

        # Image Variables
        self.image_path = None
        self.image_cv = None  # Original OpenCV image
        self.modified_image = None  # Modified image with color adjustments
        self.image_tk = None  # Image for Tkinter display

        # Frame for RGB controls
        self.frame_rgb = tk.Frame(root)
        self.frame_rgb.pack(pady=10)

        # RGB Sliders
        self.scale_red = tk.Scale(self.frame_rgb, from_=0, to=255, orient=tk.HORIZONTAL, label="Red", command=self.update_color)
        self.scale_red.set(100)  # Default = No Change
        self.scale_red.pack(side=tk.LEFT, padx=10)

        self.scale_green = tk.Scale(self.frame_rgb, from_=0, to=255, orient=tk.HORIZONTAL, label="Green", command=self.update_color)
        self.scale_green.set(100)
        self.scale_green.pack(side=tk.LEFT, padx=10)

        self.scale_blue = tk.Scale(self.frame_rgb, from_=0, to=255, orient=tk.HORIZONTAL, label="Blue", command=self.update_color)
        self.scale_blue.set(100)
        self.scale_blue.pack(side=tk.LEFT, padx=10)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image_path = file_path
            self.image_cv = cv2.imread(file_path)
            self.modified_image = self.image_cv.copy()
            self.display_image()

    def display_image(self):
        if self.modified_image is not None:
            # Resize image to fit canvas while maintaining aspect ratio
            image_rgb = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)

            # Get original dimensions
            img_width, img_height = image_pil.size

            # Calculate new dimensions while keeping the aspect ratio
            ratio = min(self.canvas_width / img_width, self.canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            image_resized = image_pil.resize((new_width, new_height), Image.LANCZOS)

            self.image_tk = ImageTk.PhotoImage(image_resized)

            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas_width//2, self.canvas_height//2, image=self.image_tk, anchor=tk.CENTER)

    def rotate_left(self):
        if self.modified_image is not None:
            self.modified_image = cv2.rotate(self.modified_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.display_image()

    def rotate_right(self):
        if self.modified_image is not None:
            self.modified_image = cv2.rotate(self.modified_image, cv2.ROTATE_90_CLOCKWISE)
            self.display_image()

    def apply_grayscale(self):
        if self.modified_image is not None:
            self.modified_image = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2GRAY)
            self.modified_image = cv2.cvtColor(self.modified_image, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels
            self.display_image()

    def update_color(self, event=None):
        """ Update image colors based on RGB sliders """
        if self.image_cv is not None:
            # Get RGB multipliers from sliders
            r_factor = self.scale_red.get() / 100
            g_factor = self.scale_green.get() / 100
            b_factor = self.scale_blue.get() / 100

            # Split image channels
            b, g, r = cv2.split(self.image_cv.astype(np.float32))

            # Apply scaling factors
            r *= r_factor
            g *= g_factor
            b *= b_factor

            # Merge channels and ensure valid range (0-255)
            self.modified_image = cv2.merge([np.clip(b, 0, 255).astype(np.uint8),
                                             np.clip(g, 0, 255).astype(np.uint8),
                                             np.clip(r, 0, 255).astype(np.uint8)])

            # Display updated image
            self.display_image()

    def save_image(self):
        if self.modified_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All Files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.modified_image)
                messagebox.showinfo("Success", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
