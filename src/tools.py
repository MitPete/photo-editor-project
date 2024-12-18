"""
Drawing and Text Tools (Person 4)

Task:
1. Add interactive tools for drawing and text overlays:
   - Implement a drawing tool using Pillow's `ImageDraw` module.
   - Create a text tool to add captions or annotations to images, with options for font, size, and color.
2. Implement an undo/redo system:
   - Maintain a stack of image states to allow users to revert or redo actions.
3. Test these tools independently to ensure accuracy and usability.

Steps:
- Use Pillow’s `ImageDraw` to draw shapes and add text.
- Create a simple history mechanism for undo/redo functionality.
- Ensure the tools integrate seamlessly with the GUI.
"""
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import io

app = Flask(__name__)

# Global variables
IMAGE_SIZE = (800, 600)
BACKGROUND_COLOR = (255, 255, 255)

# History for undo/redo
history = []
redo_stack = []

# Initialize the image
def create_blank_image():
    image = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
    return image

current_image = crate_blank_image()

# Save the image to a buffer
def save_image_to_buffer(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Save current state to history
def save_to_history():
    global current_image
    history.append(current_image.copy())

# Undo and redo
@app.route("/undo", methods=["POST"])
def undo():
    global current_image, redo_stack
    if hisroty:
        redo_stack.append(current_image.copy())
        current_image = history.pop()
    return jsonify({"status": "undo successful"})

@app.route("/redo", methods=["POST"])
def redo():
    global current_image, history
    if redo_stack:
        history.append(current_image.copy())
        current_image = redo_stack.pop()
    return jsonify({"status": "redo successful"})

# Draw shape
@app.route("/draw_shape", methods=["POST"])
def draw_shape():
    global current_image, redo_stack
    save_to_history()
    redo_stack.clear()

    data = request.json
    shape = data.get("shape")
    coords = data.get("coords")
    color = tuple(data.get("color", (0, 0, 0)))

    draw = ImageDraw.Draw(current_image)

    if shape == "rectangle":
        draw.rectangle(coords, fill=color)
    elif shape == "ellipse":
        draw.ellipse(coords, fill=color)
    elif shape == "line":
        draw.line(coords, fill-color, width=3)

    return jsonify({"status": "shape drawn successfully"})

# Add Text
@appp.route("/add_text", methods=["POST"])
def add_text():
    global current_image, redo_stack
    save_to_history()
    redo_stack.clear()

    data = request.json
    text = data.get("text", "")
    position = tuple(data.get("position", (10, 10)))
    color = tuple(data.get("color", (0, 0, 0)))

    draw = ImageDraw.Draw(current_image)
    font = ImageFont.truetype("arial.tff", 20)
    draw.text(position, text, fill=color, font=font)

    return jsonify({"status": "text added successfully"})

# Serve the current image
@app.route("/get_image", methods=["GET"])
def get_image():
    return send_file(save_image_to_buffer(current_image), mimetype="image/png")

# Serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
