"""
Core Editing Functions (Moe Karaki)

Task:
1. Implement basic editing functions:
   - `resize_image(image, width, height)` to resize the image to given dimensions.
   - `crop_image(image, box)` to crop the image based on a bounding box.
   
2. Ensure proper error handling for invalid input dimensions or paths.

3. Test each function using sample images and write standalone test scripts.

Steps:
- Use Pillow for resizing, cropping, and saving images.
- Ensure that exported images retain quality and format.
- Provide clear function signatures for integration into the GUI.
"""
import os
from PIL import Image, UnidentifiedImageError

def resize_image(image_path, width=None, height=None, scale=None, keep_aspect_ratio=False):
    """
    resize an image to the specified dimensions or scale.

    params:
    - image_path (str): path to the image file.
    - width (int, optional): desired width of the resized image.
    - height (int, optional): desired height of the resized image.
    - scale (float, optional): scale factor to resize the image (overrides width and height if provided).
    - keep_aspect_ratio (bool): whether to maintain the original aspect ratio.

    returns:
    - PIL.Image.Image: resized image object.
    """
    try:
        img = Image.open(image_path)

        # if scale isnt provided with image, calculate dimensions
        if scale is not None:
            width = int(img.width * scale)
            height = int(img.height * scale)

        if keep_aspect_ratio:
            img.thumbnail((width, height))
        else:
            if width is None or height is None:
                raise ValueError("Both width and height must be provided if keep_aspect_ratio is False.")
            img = img.resize((width, height))

        return img
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{image_path}' was not found.")
    except UnidentifiedImageError:
        raise ValueError(f"The file '{image_path}' is not a valid image.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

    
def crop_image(image_path, crop_box):
    """
    crop an image using a specified bounding box.

    params:
    - image_path (str): path to the image file.
    - crop_box (tuple): a 4-tuple defining the left, upper, right, and lower pixel coordinates.

    returns:
    - PIL.Image.Image: cropped image object.
    """
    try:
        img = Image.open(image_path)

        left, upper, right, lower = crop_box
        if left < 0 or upper < 0 or right > img.width or lower > img.height:
            print("Adjusting crop box to fit within image bounds.")
            left = max(0, left)
            upper = max(0, upper)
            right = min(img.width, right)
            lower = min(img.height, lower)
            crop_box = (left, upper, right, lower)

        cropped_img = img.crop(crop_box)
        return cropped_img
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{image_path}' was not found.")
    except UnidentifiedImageError:
        raise ValueError(f"The file '{image_path}' is not a valid image.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
    
def save_image(image, path, format="JPEG"):
    """
    save an image to the specified path in the chosen format.

    parameters:
    - image (PIL.Image.Image): the image object to save.
    - path (str): the output file path.
    - format (str): format to save the image in (e.g., "JPEG", "PNG").
    """
    try:
        image.save(path, format=format)
        print(f"Image saved successfully at {path}.")
    except Exception as e:
        raise RuntimeError(f"Failed to save the image: {e}")
    
def rotate_image(image_path, angle):
    """
    rotate an image by the specified angle.

    params:
    - image_path (str): path to the image file.
    - angle (float): the angle to rotate the image.

    returns:
    - PIL.Image.Image: rotated image object.
    """
    try:
        img = Image.open(image_path)
        rotated_img = img.rotate(angle, expand=True)
        return rotated_img
    except Exception as e:
        raise RuntimeError(f"Failed to rotate the image: {e}")



# # Dynamic path resolution
# base_dir = os.path.dirname(__file__)  # directory where this script is located
# image_path = os.path.join(base_dir, "../static/img/test_image.jpg")

# # Testing
# try:
#     resized_img = resize_image(image_path, 200, 300, keep_aspect_ratio=True)
#     resized_img.show()
#     print("Resized image displayed successfully.")
# except Exception as e:
#     print(f"Error during resizing: {e}")

# try:
#     cropped_img = crop_image(image_path, (50, 50, 300, 300))
#     cropped_img.show()
#     print("Cropped image displayed successfully.")
# except Exception as e:
#     print(f"Error during cropping: {e}")
