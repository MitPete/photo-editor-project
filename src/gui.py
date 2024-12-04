"""
Modern GUI Design (Peter Mitchell)

Tasks:
1. Add a sidebar for better navigation and additional tools.
2. Use modern colors, icons, and layout for a professional appearance.
3. Create a responsive image preview area with a toolbar for core actions.
"""

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("Photo Editor")
    root.geometry("1200x800")  # Increased size for professional look
    root.configure(bg="#1e1e1e")  # Dark mode background for a modern feel

    # Styles
    button_style = {
        "bg": "#3a3a3a",
        "fg": "white",
        "font": ("Helvetica", 12),
        "relief": "flat",
        "activebackground": "#5a5a5a",
        "activeforeground": "white",
    }

    label_style = {
        "font": ("Helvetica", 16, "bold"),
        "bg": "#1e1e1e",
        "fg": "white"
    }

    # Sidebar Frame
    sidebar = tk.Frame(root, bg="#2e2e2e", width=200, height=800)
    sidebar.pack(side="left", fill="y")

    # Add sidebar buttons
    sidebar_label = tk.Label(sidebar, text="Tools", font=("Helvetica", 14, "bold"), bg="#2e2e2e", fg="white")
    sidebar_label.pack(pady=20)

    tools = ["Upload", "Save", "Filters", "Resize", "Crop"]
    for tool in tools:
        btn = tk.Button(sidebar, text=tool, **button_style, width=20, height=2)
        btn.pack(pady=5)

    # Main Content Frame
    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(side="right", fill="both", expand=True)

    # Image Preview Area
    img_label = tk.Label(content, text="Image Preview Area", **label_style)
    img_label.pack(pady=20, expand=True)

    # Placeholder function for image upload
    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((800, 600))  # Adjust for preview size
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo, text="")
            img_label.image = photo
            root.title(f"Photo Editor - {file_path}")

    # Top Toolbar
    toolbar = tk.Frame(content, bg="#2e2e2e", height=50)
    toolbar.pack(side="top", fill="x")

    # Add toolbar buttons
    upload_button = tk.Button(toolbar, text="Upload", command=upload_image, **button_style)
    upload_button.pack(side="left", padx=5, pady=5)

    save_button = tk.Button(toolbar, text="Save", **button_style)
    save_button.pack(side="left", padx=5, pady=5)

    # Footer
    footer = tk.Label(root, text="Photo Editor App © 2024", font=("Helvetica", 10), bg="#1e1e1e", fg="#888")
    footer.pack(side="bottom", pady=10)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    create_gui()
