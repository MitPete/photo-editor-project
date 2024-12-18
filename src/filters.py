from PIL import Image, ImageEnhance, ImageFilter

def apply_grayscale(image):
    """
    Convert the image to grayscale.
    :param image: PIL Image object
    :return: Grayscale image
    """
    return image.convert("L")

def apply_sepia(image):
    """
    Apply a sepia filter to the image.
    :param image: PIL Image object
    :return: Sepia-toned image
    """
    sepia_image = image.convert("RGB")
    pixels = sepia_image.load()

    for y in range(sepia_image.height):
        for x in range(sepia_image.width):
            r, g, b = sepia_image.getpixel((x, y))

            # Sepia transformation
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            # Clamp values to 255
            sepia_image.putpixel((x, y), (min(255, tr), min(255, tg), min(255, tb)))

    return sepia_image

def apply_blur(image, radius=2):
    """
    Apply a blur effect to the image.
    :param image: PIL Image object
    :param radius: Blur intensity (default is 2)
    :return: Blurred image
    """
    return image.filter(ImageFilter.GaussianBlur(radius))

def adjust_brightness(image, factor=1.5):
    """
    Adjust the brightness of the image.
    :param image: PIL Image object
    :param factor: Brightness factor (>1 to brighten, <1 to darken)
    :return: Brightness-adjusted image
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def apply_invert(image):
    """
    Invert the colors of the image.
    :param image: PIL Image object
    :return: Inverted color image
    """
    return Image.eval(image, lambda x: 255 - x)

def apply_sharpen(image):
    """
    Apply a sharpen filter to the image.
    :param image: PIL Image object
    :return: Sharpened image
    """
    return image.filter(ImageFilter.SHARPEN)

def apply_edge_detection(image):
    """
    Apply edge detection filter to the image.
    :param image: PIL Image object
    :return: Image with edges highlighted
    """
    return image.filter(ImageFilter.FIND_EDGES)

def apply_emboss(image):
    """
    Apply an emboss effect to the image.
    :param image: PIL Image object
    :return: Embossed image
    """
    return image.filter(ImageFilter.EMBOSS)
