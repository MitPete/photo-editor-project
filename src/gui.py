import os
import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from core_functions import resize_image, crop_image
from tools import draw_shape, add_text, save_to_history, undo, redo

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
        print("Logo file not found at {logo_path}. Skipping logo display.")

    sidebar_label = tk.Label(sidebar, text="Tools", font=("Helvetica", 14, "bold"), bg="#000000", fg="white")
    sidebar_label.pack(pady=20)

    def placeholder_function():
        print("This functionality will be implemented by a teammate.")

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
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
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
                current_image = current_image.resize((width, height))
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error resizing image: {e}")

        tk.Button(dialog, text="Apply", command=apply_resize).pack()

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
        ("Filters", placeholder_function),
        ("Resize", resize_image_dialog),
        ("Crop", placeholder_function),
        ("Undo", undo_action),
        ("Redo", redo_action),
        ("Draw", draw_shape_dialog),
        ("Add Text", add_text_dialog)
    ]

    for text, command in buttons:
        btn = tk.Button(sidebar, text=text, command=command, **sidebar_button_style)
        btn.pack(pady=5)

    project_description = tk.Label(
        sidebar, 
        text="Just upload your Image... and do your thing!", 
        wraplength=150,  # Wrap text to fit the sidebar width
        justify="left",  # Center-align the text
        bg="#000000",  # Match sidebar background color
        fg="white",  # White text color
        font=("Helvetica", 12)
    )
    project_description.pack(pady=(10, 10))  # 10 pixels padding on top, 0 on bottom

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
