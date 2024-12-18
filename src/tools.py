from PIL import ImageDraw, ImageFont

# Undo/Redo History
history = []
redo_stack = []

def save_to_history(image):
    """Save the current image state to history for undo functionality."""
    history.append(image.copy())

def undo(image):
    """Undo the last action and return the previous image state."""
    if history:
        redo_stack.append(image.copy())
        return history.pop()
    print("No more undo steps available.")
    return image

def redo(image):
    """Redo the last undone action and return the next image state."""
    if redo_stack:
        history.append(image.copy())
        return redo_stack.pop()
    print("No more redo steps available.")
    return image

def draw_shape(image, shape, coords, color=(0, 0, 0)):
    """Draw shapes (rectangle, ellipse, or line) on the image."""
    draw = ImageDraw.Draw(image)
    if shape == "rectangle":
        draw.rectangle(coords, fill=color)
    elif shape == "ellipse":
        draw.ellipse(coords, fill=color)
    elif shape == "line":
        draw.line(coords, fill=color, width=3)
    return image

def add_text(image, text, position, color=(0, 0, 0), font_path="arial.ttf", font_size=20):
    """Add text annotations or captions to the image."""
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Using default font.")
        font = ImageFont.load_default()
    draw.text(position, text, fill=color, font=font)
    return image
