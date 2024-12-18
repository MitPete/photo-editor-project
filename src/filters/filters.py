"""
Filters and Effects (Person 3)

Task:
1. Develop filters and effects for the photo editor:
   - Implement grayscale, sepia, blur, brightness adjustment, and other filters.
2. Write reusable functions for each filter:
   - Example: `apply_grayscale(image)` or `apply_sepia(image)`.
3. Test each filter independently with sample images to ensure proper functionality.

Steps:
- Use Pillow and NumPy for advanced image transformations.
- Provide clear function signatures for integration into the GUI.
- Ensure filters work without degrading image quality.
"""
from PIL import Image, ImageFilter
import numpy as np
from scipy.ndimage import gaussian_filter

# Grayscale Filter
def apply_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")

# Sepia Filter
def apply_sepia(image: Image.Image) -> Image.Image:
    np_image = np.array(image)
    tr = [0.393, 0.769, 0.189]
    tg = [0.349, 0.686, 0.168]
    tb = [0.272, 0.534, 0.131]

    sepia_image = np.dot(np_image[..., :3], [tr, tg, tb])
    sepia_image = np.clip(sepia_image, 0, 255).astype("uint8")
    return Image.fromarray(sepia_image)

# Blur Filter
def apply_blur(image: Image.Image, level: str = "medium") -> Image.Image:
    levels = {
        "low": 1.0,
        "medium": 2.0,
        "high": 3.0
    }
    sigma = levels.get(level.lower(), 2.0)  # Default to "medium" if the level is invalid

    # Convert image to numpy array
    image_array = np.array(image)

    blurred_array = gaussian_filter(image_array, sigma=sigma)

    # Convert back to image
    return Image.fromarray(blurred_array)

# Brightness Adjustment
def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    np_image = np.array(image)
    adjusted = np.clip(np_image * factor, 0, 255).astype("uint8")
    return Image.fromarray(adjusted)