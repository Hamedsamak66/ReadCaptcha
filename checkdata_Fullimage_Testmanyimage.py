import requests
from PIL import Image
import os
import cv2
import numpy as np
import shutil
import sqlite3

''' alter database'''



conn = sqlite3.connect('captcha_results.db')


# ایجاد جدول برای ذخیره نتایج
def create_table():
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_name TEXT NOT NULL,
                part1_sum TEXT,
                part2_sum TEXT,
                total_sum INTEGER
            );
        ''')
# تابع برای درج نتایج در جدول
def insert_result(image_name, part1_sum, part2_sum, total_sum):
    with conn:
        conn.execute('''
            INSERT INTO results (image_name, part1_sum, part2_sum, total_sum)
            VALUES (?, ?, ?, ?);
        ''', (image_name, part1_sum, part2_sum, total_sum))
create_table()
def is_image_mostly_white(image_path, white_threshold=0.95):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image could not be loaded.")
        
        # Calculate the total number of pixels
        total_pixels = img.shape[0] * img.shape[1]
        
        # Create a mask where all white pixels are marked
        white_mask = cv2.inRange(img, (255, 255, 255), (255, 255, 255))
        
        # Calculate the number of white pixels
        white_pixels = cv2.countNonZero(white_mask)
        
        # Calculate the ratio of white pixels
        white_ratio = white_pixels / total_pixels
        return white_ratio >= white_threshold
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def is_image_white(image_path):
    try:
        # Load the image
        img = cv2.imread(image_path)

        # Validate that the image is loaded
        if img is None:
            raise ValueError("Image could not be loaded.")

        # Check if all pixels are white (255, 255, 255)
        if np.all(img == 255):
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def remove_lines_and_background(image):
    # تبدیل تصویر به فضای رنگی RGB (در صورت وجود کانال آلفا)
    if image.shape[2] == 4:  # بررسی وجود کانال آلفا
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # تبدیل تصویر به فضای رنگی HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # تعریف محدوده رنگ برای حذف خطوط (تنظیم محدوده برای خطوط)
    lower_bound = np.array([0, 0, 0])  # حد پایین رنگ خطوط
    upper_bound = np.array([180, 255, 150])  # حد بالا رنگ خطوط

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

def find_white_line(image, start_index, threshold=0.9):
    height, width = image.shape[:2]
    left_index = start_index
    right_index = start_index

    while left_index >= 0 or right_index < width:
        # بررسی ستون سمت راست
        if right_index < width:
            white_pixels_right = np.sum(image[:, right_index] == 255)
            if white_pixels_right == height or white_pixels_right / height >= threshold:
                return right_index
        
        # بررسی ستون سمت چپ
        if left_index >= 0:
            white_pixels_left = np.sum(image[:, left_index] == 255)
            if white_pixels_left == height or white_pixels_left / height >= threshold:
                return left_index

        right_index += 1
        left_index -= 1

    return None


cut_point1_x = 63  # نقطه اول
cut_point2_x = 117  # نقطه دوم
for img in range(1,5000):
    image = Image.open(f'images/{img}.png')
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
    number = ''
    for i in range(1,3):
        number = ''
        for j in range(1,3):
            if is_image_mostly_white(f'{img}_{i}_{j}.png'):
                continue
            else:    
                url = 'http://127.0.0.1:5000/predict'
                f = open(f'{img}_{i}_{j}.png', 'rb')
                files = {'file': f}
                response = requests.post(url, files=files)
                
                res = response.json()["predicted_class"]
                number = str(number) + str(res)
                
        stack.append(number)
        if i == 1:
            stack.append('+')
            temp = 0
    f.close()
    # متغیر برای نگه‌داری مجموع دو بخش
    sum_part1 = 0
    sum_part2 = 0
    #print(stack)
    #exit()
    # نشانگر وضعیت برای تعیین اینکه کدام بخش در حال پردازش است
    first_part = True
    for item in stack:
        if item == '+':
            # زمانی که به عملگر جمع می‌رسیم، بخش دوم شروع می‌شود
            first_part = False
            continue
        if first_part:
            sum_part1 = item
        else:
            sum_part2 = item


    '''
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
    '''
    # محاسبه مجموع نهایی
    if(sum_part1 == '' or sum_part2 == ''):
        total = 0
    else:    
        total = int(sum_part1) + int(sum_part2)

    # نمایش نتایج
    print(f"مجموع بخش اول: {sum_part1}")
    print(f"مجموع بخش دوم: {sum_part2}")
    print(f"مجموع کلی: {total}")
    #print(stack)
    shutil.copy2(f'images/{img}.png', f'images_for_check/{img}_{sum_part1}+{sum_part2}={total}.png')
    insert_result(img, sum_part1, sum_part2, total)
    os.remove(f'{img}_1_2.png')
    os.remove(f'{img}_1_1.png')
    os.remove(f'{img}_1.png')
    os.remove(f'{img}_2.png')
    os.remove(f'{img}_2_1.png')
    os.remove(f'{img}_2_2.png')
    #exit()
    