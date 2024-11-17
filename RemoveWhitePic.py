from PIL import Image
import os

def is_white_image(image_path):
    with Image.open(image_path) as img:
        gray_img = img.convert('L')  # تبدیل به خاکستری
        histogram = gray_img.histogram()
        pixels = sum(histogram)
        white_pixels = histogram[255]
        if white_pixels / pixels > 0.95:  # اگر بیش از ۹۵٪ سفید است
            return True
    return False

directory = "labeling_project/image_labeler/static/images/"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        file_path = os.path.join(directory, filename)
        if is_white_image(file_path):
            os.remove(file_path)
            print(f"Removed {filename}")
