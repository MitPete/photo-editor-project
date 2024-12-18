import unittest
import os
from PIL import Image
from filters.filters import (
    apply_grayscale, 
    apply_sepia, 
    apply_blur, 
    adjust_brightness
)

class TestImageFilters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load a sample image for all tests
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this test file
        image_path = os.path.join(current_dir, "../images/landscape2.jpg")  # Adjust path to the image
        
        # Open the image
        cls.sample_image = Image.open(image_path)
        cls.sample_image.load()  # Ensure the image is fully loaded

    def test_grayscale(self):
        gray_image = apply_grayscale(self.sample_image)
        self.assertEqual(gray_image.mode, "L")

    def test_sepia(self):
        sepia_image = apply_sepia(self.sample_image)
        self.assertEqual(sepia_image.mode, "RGB")

    def test_blur(self):
        # Test predefined levels
        blurred_image_low = apply_blur(self.sample_image, "low")
        blurred_image_medium = apply_blur(self.sample_image, "medium")
        blurred_image_high = apply_blur(self.sample_image, "high")

        # Assert that the images are still valid
        self.assertEqual(blurred_image_low.mode, "RGB")
        self.assertEqual(blurred_image_medium.mode, "RGB")
        self.assertEqual(blurred_image_high.mode, "RGB")

    def test_brightness(self):
        bright_image = adjust_brightness(self.sample_image, 1.5)
        self.assertEqual(bright_image.mode, "RGB")

if __name__ == "__main__":
    unittest.main()
