import requests
from PIL import Image
import os
import cv2
import numpy as np


def remove_lines_and_background(image):
    # تبدیل تصویر به فضای رنگی RGB (در صورت وجود کانال آلفا)
    if image.shape[2] == 4:  # بررسی وجود کانال آلفا
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # تبدیل تصویر به فضای رنگی HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # تعریف محدوده رنگ برای حذف خطوط (تنظیم محدوده برای خطوط)
    lower_bound = np.array([0, 0, 0])  # حد پایین رنگ خطوط
    upper_bound = np.array([180, 255, 120])  # حد بالا رنگ خطوط

    # شناسایی خطوط با ماسک‌گذاری
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # معکوس کردن ماسک برای نگه‌داشتن اعداد
    inverted_mask = cv2.bitwise_not(mask)

    # حذف نویزها با عملیات مورفولوژی
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_CLOSE, kernel)

    # اعمال ماسک روی تصویر اصلی
    result = cv2.bitwise_and(image, image, mask=cleaned_mask)

    # تبدیل به grayscale
    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

    # اعمال باینری برای داشتن پس‌زمینه سفید و اعداد سیاه
    _, binary_img = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)

    return binary_img

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

cut_point1_x = 63  # نقطه اول
cut_point2_x = 117  # نقطه دوم
img = 22160
image = Image.open(f'images/images/{img}.png')
width, height = image.size
# برش تصویر
slice1_box = (0, 0, cut_point1_x, height)
slice2_box = (cut_point1_x, 0, cut_point2_x, height)

slice1 = image.crop(slice1_box)
slice2 = image.crop(slice2_box)

# ذخیره برش‌ها به عنوان فایل‌های جدید
slice1.save(f'{img}_1.png')
slice2.save(f'{img}_2.png')
for i in range(1,3):
    # خواندن تصویر ورودی
    image = cv2.imread(f'{img}_{i}.png', cv2.IMREAD_UNCHANGED)
    # حذف خطوط و پس‌زمینه
    processed_image = remove_lines_and_background(image)
    # معکوس کردن رنگ‌ها
    processed_image = cv2.bitwise_not(processed_image)
    # ذخیره تصویر خروجی
    cv2.imwrite(f'{img}_{i}.png', processed_image)
    ## SPLIT IMAGE LEFT & RIGHT
    # بارگذاری تصویر
    image_path = f'{img}_{i}.png'  # مسیر تصویر خود را بگذارید
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
            cv2.imwrite(f'{img}_{i}_1.png', left_image)
            cv2.imwrite(f'{img}_{i}_2.png', right_image)
stack = []
for i in range(1,3):
    for j in range(1,3):
        url = 'http://127.0.0.1:5000/predict'
        files = {'file': open(f'{img}_{i}_{j}.png', 'rb')}
        response = requests.post(url, files=files)
        print(response.json())
        if j == 1:
            temp = str(response.json())
        if j == 2:
            stack.append(str(temp) + str(response.json()))
    if i == 1:
        stack.append('+')
        temp = 0

# متغیر برای نگه‌داری مجموع دو بخش
sum_part1 = 0
sum_part2 = 0

# نشانگر وضعیت برای تعیین اینکه کدام بخش در حال پردازش است
first_part = True

for item in stack:
    if item == '+':
        # زمانی که به عملگر جمع می‌رسیم، بخش دوم شروع می‌شود
        first_part = False
        continue

    if isinstance(item, dict) and 'predicted_class' in item:
        # اگر آیتم یک دیکشنری با کلید 'predicted_class' باشد
        if first_part:
            sum_part1 += item['predicted_class']
        else:
            sum_part2 += item['predicted_class']

# محاسبه مجموع نهایی
total = sum_part1 + sum_part2

# نمایش نتایج
print(f"مجموع بخش اول: {sum_part1}")
print(f"مجموع بخش دوم: {sum_part2}")
print(f"مجموع کلی: {total}")
print(stack)
        

    