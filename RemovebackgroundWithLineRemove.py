import os
import cv2
import numpy as np

# پوشه حاوی تصاویر ورودی
input_folder = "AfterCrop"
# پوشه برای ذخیره تصاویر خروجی
output_folder = "ProcessedImages"

# بررسی وجود پوشه خروجی
os.makedirs(output_folder, exist_ok=True)

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

# پردازش هر تصویر در پوشه ورودی
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.png')) and not file_name.endswith("_3.png"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # خواندن تصویر ورودی
        image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

        # حذف خطوط و پس‌زمینه
        processed_image = remove_lines_and_background(image)
        # معکوس کردن رنگ‌ها
        processed_image = cv2.bitwise_not(processed_image)
        # ذخیره تصویر خروجی
        cv2.imwrite(output_path, processed_image)

print("پردازش تصاویر کامل شد!")
