import os
import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from core_functions import resize_image, crop_image
from tools import draw_shape, add_text, save_to_history, undo, redo
from filters import apply_grayscale, apply_sepia, apply_blur, adjust_brightness, apply_invert, apply_sharpen, apply_edge_detection, apply_emboss

def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("The Editor.")
    root.geometry("1200x800")
    root.configure(bg="#1e1e1e")

    current_image = None

    sidebar_button_style = {
        "bg": "#2e2e2e",
        "fg": "white",
        "font": ("Helvetica", 12),
        "relief": "flat",
        "activebackground": "#5a5a5a",
        "activeforeground": "white",
        "width": 15,
        "height": 1
    }

    toolbar_button_style = {
        "bg": "#000000",
        "fg": "white",
        "font": ("Helvetica", 12),
        "relief": "flat",
        "activebackground": "#444444",
        "activeforeground": "white"
    }
    label_style = {"font": ("Helvetica", 16, "bold"), "bg": "#1e1e1e", "fg": "white"}

    base_dir = os.path.dirname(__file__)
    logo_path = os.path.join(base_dir, "../static/img/logo.png")

    sidebar = tk.Frame(root, bg="#000000", width=300)
    sidebar.pack(side="left", fill="y")

    try:
        logo_image = Image.open(logo_path)
        logo_image.thumbnail((150, 150))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(sidebar, image=logo_photo, bg="#000000")
        logo_label.image = logo_photo
        logo_label.pack(pady=10)
    except FileNotFoundError:
        print(f"Logo file not found at {logo_path}. Skipping logo display.")

    sidebar_label = tk.Label(sidebar, text="Tools", font=("Helvetica", 14, "bold"), bg="#000000", fg="white")
    sidebar_label.pack(pady=20)

    def update_preview(image):
        nonlocal current_image
        current_image = image
        img = current_image.copy()
        img.thumbnail((800, 600))
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo

    def upload_image():
        nonlocal current_image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ("*.png", "*.jpg", "*.jpeg"))]
)
        if file_path:
            current_image = Image.open(file_path)
            update_preview(current_image)
            root.title(f"Photo Editor - {file_path}")

    def save_image():
        if current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                current_image.save(file_path)
                print(f"Image saved at {file_path}")

    def undo_action():
        nonlocal current_image
        if current_image:
            current_image = undo(current_image)
            update_preview(current_image)

    def redo_action():
        nonlocal current_image
        if current_image:
            current_image = redo(current_image)
            update_preview(current_image)

    # Dialog for applying filters
    def apply_filter_dialog():
        if not current_image:
            print("No image to apply filters!")
            return

        dialog = Toplevel(root)
        dialog.title("Filters and Effects")

        def apply_filter(filter_function, *args):
            nonlocal current_image
            save_to_history(current_image)
            current_image = filter_function(current_image, *args)
            update_preview(current_image)

        tk.Button(dialog, text="Grayscale", command=lambda: apply_filter(apply_grayscale)).pack(pady=5)
        tk.Button(dialog, text="Sepia", command=lambda: apply_filter(apply_sepia)).pack(pady=5)
        tk.Button(dialog, text="Invert", command=lambda: apply_filter(apply_invert)).pack(pady=5)
        tk.Button(dialog, text="Sharpen", command=lambda: apply_filter(apply_sharpen)).pack(pady=5)
        tk.Button(dialog, text="Edge Detection", command=lambda: apply_filter(apply_edge_detection)).pack(pady=5)
        tk.Button(dialog, text="Emboss", command=lambda: apply_filter(apply_emboss)).pack(pady=5)

        # Blur with user input
        tk.Label(dialog, text="Blur Radius:").pack()
        blur_entry = tk.Entry(dialog)
        blur_entry.pack()
        tk.Button(dialog, text="Apply Blur", command=lambda: apply_filter(apply_blur, int(blur_entry.get()))).pack(pady=5)

        # Brightness with user input
        tk.Label(dialog, text="Brightness Factor (e.g., 1.5):").pack()
        brightness_entry = tk.Entry(dialog)
        brightness_entry.pack()
        tk.Button(dialog, text="Adjust Brightness", command=lambda: apply_filter(adjust_brightness, float(brightness_entry.get()))).pack(pady=5)

    # Dialog for resizing the image
    def resize_image_dialog():
        if not current_image:
            print("No image to resize!")
            return

        dialog = Toplevel(root)
        dialog.title("Resize Image")

        tk.Label(dialog, text="Width:").pack()
        width_entry = tk.Entry(dialog)
        width_entry.pack()

        tk.Label(dialog, text="Height:").pack()
        height_entry = tk.Entry(dialog)
        height_entry.pack()

        def apply_resize():
            nonlocal current_image
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                save_to_history(current_image)
                # Use resize_image from core_functions to ensure consistency
                current_image = current_image.resize((width, height))
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error resizing image: {e}")

        tk.Button(dialog, text="Apply", command=apply_resize).pack()

    # Dialog for cropping the image
    def crop_image_dialog():
        if not current_image:
            print("No image to crop!")
            return

        dialog = Toplevel(root)
        dialog.title("Crop Image")

        tk.Label(dialog, text="Crop Coordinates (x1,y1,x2,y2):").pack()
        coords_entry = tk.Entry(dialog)
        coords_entry.pack()

        def apply_crop():
            nonlocal current_image
            try:
                coords = tuple(map(int, coords_entry.get().split(",")))
                if len(coords) != 4:
                    raise ValueError("Please enter four integers separated by commas.")
                save_to_history(current_image)
                current_image = crop_image(current_image, coords)
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error cropping image: {e}")

        tk.Button(dialog, text="Apply", command=apply_crop).pack()

    # Dialog for drawing shapes on the image
    def draw_shape_dialog():
        if not current_image:
            print("No image to draw on!")
            return

        dialog = Toplevel(root)
        dialog.title("Draw Shape")

        tk.Label(dialog, text="Shape: (rectangle, ellipse, line)").pack()
        shape_entry = tk.Entry(dialog)
        shape_entry.pack()

        tk.Label(dialog, text="Coordinates (x1,y1,x2,y2):").pack()
        coords_entry = tk.Entry(dialog)
        coords_entry.pack()

        tk.Label(dialog, text="Color (R,G,B):").pack()
        color_entry = tk.Entry(dialog)
        color_entry.pack()

        def apply_draw():
            nonlocal current_image
            try:
                shape = shape_entry.get()
                coords = tuple(map(int, coords_entry.get().split(",")))
                color = tuple(map(int, color_entry.get().split(",")))
                save_to_history(current_image)
                current_image = draw_shape(current_image, shape, coords, color)
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error drawing shape: {e}")

        tk.Button(dialog, text="Apply", command=apply_draw).pack()

    # Dialog for adding text to the image
    def add_text_dialog():
        if not current_image:
            print("No image to add text!")
            return

        dialog = Toplevel(root)
        dialog.title("Add Text")

        tk.Label(dialog, text="Text:").pack()
        text_entry = tk.Entry(dialog)
        text_entry.pack()

        tk.Label(dialog, text="Position (x,y):").pack()
        position_entry = tk.Entry(dialog)
        position_entry.pack()

        tk.Label(dialog, text="Color (R,G,B):").pack()
        color_entry = tk.Entry(dialog)
        color_entry.pack()

        def apply_text():
            nonlocal current_image
            try:
                text = text_entry.get()
                position = tuple(map(int, position_entry.get().split(",")))
                color = tuple(map(int, color_entry.get().split(",")))
                save_to_history(current_image)
                current_image = add_text(current_image, text, position, color)
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error adding text: {e}")

        tk.Button(dialog, text="Apply", command=apply_text).pack()

    buttons = [
        ("Upload", upload_image),
        ("Save", save_image),
        ("Filters", apply_filter_dialog),
        ("Resize", resize_image_dialog),
        ("Crop", crop_image_dialog),
        ("Undo", undo_action),
        ("Redo", redo_action),
        ("Draw", draw_shape_dialog),
        ("Add Text", add_text_dialog)
    ]

    for text, command in buttons:
        btn = tk.Button(sidebar, text=text, command=command, **sidebar_button_style)
        btn.pack(pady=5)

    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", fill="both", expand=True)

    img_label = tk.Label(content, text="Image Preview Area", **label_style)
    img_label.pack(pady=20, expand=True)

    toolbar = tk.Frame(content, bg="#2e2e2e", height=50)
    toolbar.pack(side="bottom", fill="x")

    upload_btn_toolbar = tk.Button(toolbar, text="Upload", command=upload_image, **toolbar_button_style)
    upload_btn_toolbar.pack(side="left", padx=5, pady=5)

    save_btn_toolbar = tk.Button(toolbar, text="Save", command=save_image, **toolbar_button_style)
    save_btn_toolbar.pack(side="left", padx=5, pady=5)

    footer = tk.Label(root, text="The Editor. © 2024", font=("Helvetica", 10), bg="#1e1e1e", fg="#888")
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
