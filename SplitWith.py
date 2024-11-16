import cv2
import numpy as np
import os

def find_white_line(image, start_index):
    height, width = image.shape[:2]
    left_index = start_index
    right_index = start_index

    while left_index >= 0 or right_index < width:
        if right_index < width and np.all(image[:, right_index] == 255):
            return right_index
        if left_index >= 0 and np.all(image[:, left_index] == 255):
            return left_index

        right_index += 1
        left_index -= 1

    return None

def remove_white_border(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)
    coords = np.column_stack(np.where(binary_mask > 0))
    x, y, w, h = cv2.boundingRect(coords)
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

os.makedirs('AfterSplit', exist_ok=True)  # مطمئن شوید مسیر وجود دارد

for i in range(1, 500):
    for j in range(1, 3):
        image_path = f'ProcessedImages/{i}_{j}.png'
        image = cv2.imread(image_path)

        if image is None:
            print(f"[خطا] تصویر بارگذاری نشد: {image_path}")
            continue

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        middle_column = gray_image.shape[1] // 2
        border_position = find_white_line(gray_image, middle_column)

        if border_position is not None:
            print(f"[اطلاعات] مرز در موقعیت: {border_position} برای تصویر {image_path}")

            left_image = image[:, :border_position]
            right_image = image[:, border_position:]

            if left_image.size == 0 or right_image.size == 0:
                print(f"[خطا] مشکلی در تقسیم تصویر وجود دارد: {image_path}")
                continue

            left_image = remove_white_border(left_image)
            right_image = remove_white_border(right_image)

            # بررسی اندازه تصاویر بعد از حذف فضای سفید
            if left_image.size == 0 or right_image.size == 0:
                print(f"[خطا] تصویر بعد از حذف فضای سفید خالی است: {image_path}")
                continue

            cv2.imwrite(f'AfterSplit/{i}_{j}_Left.png', left_image)
            cv2.imwrite(f'AfterSplit/{i}_{j}_Right.png', right_image)
            print(f"[اطلاعات] تصویر به دو تکه تقسیم و ذخیره شد: {image_path}")
        else:
            print(f"[هشدار] هیچ مرز سفیدی پیدا نشد: {image_path}")
