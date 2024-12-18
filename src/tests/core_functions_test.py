import unittest
import os
from PIL import Image
from core_functions import resize_image, crop_image, save_image, rotate_image

class TestCoreFunctions(unittest.TestCase):
    def setUp(self):
        self.test_image_path = "test_image.jpg"
        self.output_image_path = "output_image.jpg"
        self.test_image_size = (400, 300)
        self.test_image = Image.new("RGB", self.test_image_size, color="blue")
        self.test_image.save(self.test_image_path)

    def tearDown(self):
        #deletes any created test images or output files.
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.output_image_path):
            os.remove(self.output_image_path)

    def test_resize_image(self):
        #test resizing an image to specific dimensions.
        resized_image = resize_image(self.test_image_path, width=200, height=150)
        self.assertEqual(resized_image.size, (200, 150))

    def test_resize_image_aspect_ratio(self):
        #test resizing an image while maintaining aspect ratio.
        resized_image = resize_image(self.test_image_path, width=200, height=150, keep_aspect_ratio=True)
        self.assertTrue(resized_image.size[0] <= 200 and resized_image.size[1] <= 150)

    def test_resize_image_with_scale(self):
        #test resizing an image using a scale factor
        resized_image = resize_image(self.test_image_path, scale=0.5)
        expected_size = (int(self.test_image_size[0] * 0.5), int(self.test_image_size[1] * 0.5))
        self.assertEqual(resized_image.size, expected_size)

    def test_crop_image(self):
        #test cropping an image with a valid bounding box.
        crop_box = (50, 50, 250, 200)
        cropped_image = crop_image(self.test_image_path, crop_box)
        self.assertEqual(cropped_image.size, (200, 150))

    def test_crop_image_out_of_bounds(self):
        #test cropping an image with a bounding box that exceeds the image's dimensions.
        crop_box = (-10, -10, 500, 500)
        cropped_image = crop_image(self.test_image_path, crop_box)
        self.assertEqual(cropped_image.size, (400, 300))  

    def test_save_image(self):
        #test saving an image in a specific format
        resized_image = resize_image(self.test_image_path, width=200, height=150)
        save_image(resized_image, self.output_image_path, format="PNG")
        self.assertTrue(os.path.exists(self.output_image_path))

    def test_rotate_image(self):
        #test rotating an image by a specified angle
        rotated_image = rotate_image(self.test_image_path, angle=90)
        self.assertEqual(rotated_image.size, (300, 400))  

if __name__ == "__main__":
    unittest.main()