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
    upper_bound = np.array([180, 255, 160])  # حد بالا رنگ خطوط

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



# خواندن تصویر ورودی
image = cv2.imread('AfterCrop/4_1.png', cv2.IMREAD_UNCHANGED)

# حذف خطوط و پس‌زمینه
processed_image = remove_lines_and_background(image)
# معکوس کردن رنگ‌ها
processed_image = cv2.bitwise_not(processed_image)
# ذخیره تصویر خروجی
cv2.imwrite('out.png', processed_image)

print("پردازش تصاویر کامل شد!")
