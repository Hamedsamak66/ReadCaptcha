import os
import io  # اضافه کردن این خط برای وارد کردن کتابخانه io
from rembg import remove
from PIL import Image
import numpy as np
import cv2

# پوشه حاوی تصاویر ورودی
input_folder = "AfterCrop"
# پوشه برای ذخیره تصاویر خروجی
output_folder = "AfterBackground"

# بررسی وجود پوشه خروجی
os.makedirs(output_folder, exist_ok=True)

# پردازش هر تصویر در پوشه
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # باز کردن تصویر
        with open(input_path, "rb") as input_file:
            input_data = input_file.read()

        # حذف پس‌زمینه
        output_data = remove(input_data)

        # تبدیل داده‌های خروجی به تصویر
        img = Image.open(io.BytesIO(output_data))

        # تبدیل به numpy array
        img_np = np.array(img)

        # تبدیل تصویر به grayscale (سیاه و سفید)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)

        # اعمال آستانه‌گذاری برای تبدیل به 0 و 255
        # مقادیر کوچک‌تر از آستانه به 255 (سفید) و مقادیر بزرگتر به 0 (سیاه)
        _, binary_img = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY_INV)

        # ذخیره تصویر باینری
        cv2.imwrite(output_path, binary_img)

print("حذف پس‌زمینه و ذخیره تصاویر باینری کامل شد!")
