import cv2
import numpy as np

def find_white_line(image, start_index):
    height, width = image.shape[:2]
    left_index = start_index
    right_index = start_index

    while left_index >= 0 or right_index < width:
        # بررسی ستون سمت راست
        if right_index < width and np.all(image[:, right_index] == 255):
            return right_index
        # بررسی ستون سمت چپ
        if left_index >= 0 and np.all(image[:, left_index] == 255):
            return left_index

        right_index += 1
        left_index -= 1

    return None
for i in range(1, 500):
    for j in range (1,3):
        # بارگذاری تصویر
        image_path = f'ProcessedImages/{i}_{j}.png'  # مسیر تصویر خود را بگذارید
        image = cv2.imread(image_path)

        if image is None:
            print("مشکلی در بارگذاری تصویر وجود دارد.")
            exit()

        # تبدیل تصویر به خاکستری
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # شروع جستجو از وسط تصویر
        middle_column = gray_image.shape[1] // 2

        # پیدا کردن مکان خط سفید
        border_position = find_white_line(gray_image, middle_column)

        if border_position is not None:
            print("مرز در موقعیت:", border_position)

            # تقسیم تصویر به دو تکه
            left_image = image[:, :border_position]
            right_image = image[:, border_position:]

            # بررسی اینکه آیا تصاویر خالی هستند
            if left_image.size == 0 or right_image.size == 0:
                print("مشکلی در تقسیم تصویر وجود دارد.")
            else:
                # ذخیره تکه‌های تصویر
                cv2.imwrite(f'AfterSplit/{i}_{j}_Left.png', left_image)
                cv2.imwrite(f'AfterSplit/{i}_{j}_Right.png', right_image)
                print("تصویر به دو تکه تقسیم شد!")
        else:
            print("هیچ مرز سفیدی پیدا نشد.")
