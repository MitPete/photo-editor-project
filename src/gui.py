import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("Photo Editor")
    root.geometry("1200x800")  # Increased size for professional look
    root.configure(bg="#1e1e1e")  # Dark mode background for a modern feel

    # Global variable to store the current image
    current_image = None

    # Styles for sidebar buttons
    sidebar_button_style = {
        "bg": "#2e2e2e",  # Default background color
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

    label_style = {
        "font": ("Helvetica", 16, "bold"),
        "bg": "#1e1e1e",
        "fg": "white"
    }

    # Sidebar Frame
    sidebar = tk.Frame(root, bg="#2e2e2e", width=200, height=800)
    sidebar.pack(side="left", fill="y")

    # Sidebar label
    sidebar_label = tk.Label(sidebar, text="Tools", font=("Helvetica", 14, "bold"), bg="#2e2e2e", fg="white")
    sidebar_label.pack(pady=20)

    # Function to upload an image
    def upload_image():
        nonlocal current_image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            current_image = Image.open(file_path)
            update_preview()
            root.title(f"Photo Editor - {file_path}")

    # Function to save the current image
    def save_image():
        if current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                current_image.save(file_path)
                print(f"Image saved at {file_path}")

    # Function to update the preview area
    def update_preview():
        if current_image:
            img = current_image.copy()
            img.thumbnail((800, 600))  # Resize for preview
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo, text="")
            img_label.image = photo

    # Function to apply hover effect
    def on_hover(event):
        event.widget.config(bg="#444")  # Hover background color

    def on_leave(event):
        event.widget.config(bg=sidebar_button_style["bg"])  # Restore original background color

    # Sidebar buttons
    buttons = [
        ("Upload", upload_image),
        ("Save", save_image),
        ("Filters", None),  # Placeholder for Filters functionality
        ("Resize", None),   # Placeholder for Resize functionality
        ("Crop", None),     # Placeholder for Crop functionality
    ]

    for text, command in buttons:
        btn = tk.Button(sidebar, text=text, command=command, **sidebar_button_style)
        btn.pack(pady=5)

        # Add hover effect to the button
        btn.bind("<Enter>", on_hover)  # Mouse enters the button
        btn.bind("<Leave>", on_leave)  # Mouse leaves the button

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

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    create_gui()
