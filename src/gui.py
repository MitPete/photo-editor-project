import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from core_functions import resize_image, crop_image  # Import core functions


def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("Photo Editor")
    root.geometry("1200x800")
    root.configure(bg="#1e1e1e")

    # Global variable to store the current image
    current_image = None

    # Styles for sidebar buttons
    sidebar_button_style = {
        "bg": "#2e2e2e",
        "fg": "white",
        "font": ("Helvetica", 12),
        "relief": "flat",
        "activebackground": "#5a5a5a",
        "activeforeground": "white",
        "width": 20,
        "height": 2
    }

    # Styles for toolbar buttons
    toolbar_button_style = {
        "bg": "#3a3a3a",
        "fg": "white",
        "font": ("Helvetica", 12),
        "relief": "flat",
        "activebackground": "#5a5a5a",
        "activeforeground": "white"
    }
    label_style = {"font": ("Helvetica", 16, "bold"), "bg": "#1e1e1e", "fg": "white"}

    # Sidebar Frame
    sidebar = tk.Frame(root, bg="#2e2e2e", width=200)
    sidebar.pack(side="left", fill="y")

    # Sidebar label
    sidebar_label = tk.Label(sidebar, text="Tools", font=("Helvetica", 14, "bold"), bg="#2e2e2e", fg="white")
    sidebar_label.pack(pady=20)

    # Placeholder function for unfinished features
    def placeholder_function():
        print("This functionality will be implemented by a teammate.")

    # Function to update the image preview
    def update_preview(image):
        nonlocal current_image
        current_image = image
        img = current_image.copy()
        img.thumbnail((800, 600))
        photo = ImageTk.PhotoImage(img)
        img_label.config(image=photo)
        img_label.image = photo

    # Upload Image
    def upload_image():
        nonlocal current_image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            current_image = Image.open(file_path)
            update_preview(current_image)
            root.title(f"Photo Editor - {file_path}")

    # Save Image
    def save_image():
        if current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                current_image.save(file_path)
                print(f"Image saved at {file_path}")

    # Crop Image
    def crop_image_dialog():
        if not current_image:
            print("No image to crop!")
            return

        dialog = Toplevel(root)
        dialog.title("Crop Image")

        tk.Label(dialog, text="Left:").pack()
        left_entry = tk.Entry(dialog)
        left_entry.pack()

        tk.Label(dialog, text="Top:").pack()
        top_entry = tk.Entry(dialog)
        top_entry.pack()

        tk.Label(dialog, text="Right:").pack()
        right_entry = tk.Entry(dialog)
        right_entry.pack()

        tk.Label(dialog, text="Bottom:").pack()
        bottom_entry = tk.Entry(dialog)
        bottom_entry.pack()

        def apply_crop():
            nonlocal current_image
            try:
                crop_box = (
                    int(left_entry.get()), int(top_entry.get()),
                    int(right_entry.get()), int(bottom_entry.get())
                )
                current_image = current_image.crop(crop_box)  # Use crop directly
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error cropping image: {e}")

        tk.Button(dialog, text="Apply", command=apply_crop).pack()

    # Resize Image
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
                current_image = current_image.resize((width, height))  # Use resize directly
                update_preview(current_image)
                dialog.destroy()
            except Exception as e:
                print(f"Error resizing image: {e}")

        tk.Button(dialog, text="Apply", command=apply_resize).pack()

    # Hover effect for sidebar buttons
    def on_hover(event):
        event.widget.config(bg="#444")

    def on_leave(event):
        event.widget.config(bg=sidebar_button_style["bg"])

    # Sidebar buttons
    buttons = [
        ("Upload", upload_image),
        ("Save", save_image),
        ("Filters", placeholder_function),
        ("Resize", resize_image_dialog),
        ("Crop", crop_image_dialog),
        ("Undo", placeholder_function),
        ("Redo", placeholder_function),
        ("Draw", placeholder_function),
        ("Add Text", placeholder_function)
    ]

    for text, command in buttons:
        btn = tk.Button(sidebar, text=text, command=command, **sidebar_button_style)
        btn.pack(pady=5)
        btn.bind("<Enter>", on_hover)
        btn.bind("<Leave>", on_leave)

    # Main Content Frame
    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", fill="both", expand=True)

    # Image Preview Area
    img_label = tk.Label(content, text="Image Preview Area", **label_style)
    img_label.pack(pady=20, expand=True)

    # Toolbar
    toolbar = tk.Frame(content, bg="#2e2e2e", height=50)
    toolbar.pack(side="bottom", fill="x")

    upload_btn_toolbar = tk.Button(toolbar, text="Upload", command=upload_image, **toolbar_button_style)
    upload_btn_toolbar.pack(side="left", padx=5, pady=5)

    save_btn_toolbar = tk.Button(toolbar, text="Save", command=save_image, **toolbar_button_style)
    save_btn_toolbar.pack(side="left", padx=5, pady=5)

    # Footer
    footer = tk.Label(root, text="Photo Editor App © 2024", font=("Helvetica", 10), bg="#1e1e1e", fg="#888")
    footer.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
