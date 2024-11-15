import cv2
import numpy as np
import matplotlib.pyplot as plt

def rgb_to_hsv(r, g, b):
    rgb = np.uint8([[[r, g, b]]])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return hsv[0][0]  # برگشت به فرمت (H, S, V)
def get_hsv_range(h, s, v, hue_range=20, sat_range=50, val_range=60):
    # محاسبه محدوده با استفاده از فاصله
    lower = np.array([max(0, h - hue_range), max(0, s - sat_range), max(0, v - val_range)])
    upper = np.array([min(179, h + hue_range), min(255, s + sat_range), min(255, v + val_range)])
    return lower, upper
def calculate_hsv_range_from_rgb(r, g, b):
    h, s, v = rgb_to_hsv(r, g, b)
    print(h,s,v)
    lower, upper = get_hsv_range(h, s, v)
    return lower, upper



# خواندن تصویر
img = cv2.imread(f'AfterCrop/3_1.png')
(b, g, r) = img[0, 0]
print(f'r={r},g={g},b={b}')
lower, upper = calculate_hsv_range_from_rgb(r, g, b)
print("Lower:", lower, ", Upper:", upper)




# مقداردهشی دقیق محدوده‌های رنگی
#lower = np.array([5, 90, 90])  # مقدار مثال
#upper = np.array([120, 255, 255])  # مقدار مثال

# تبدیل تصویر به فضای رنگی HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ایجاد ماسک برای بخش رنگ خاص
mask = cv2.inRange(hsv, lower, upper)

# استفاده از فیلتر گوسین برای نرم‌سازی
blurred = cv2.GaussianBlur(mask, (5, 5), 0)

# کاهش اندازه کرنل برای عملیات مورفولوژیکی
kernel = np.ones((2, 2), np.uint8)
mask_cleaned = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

# باینری‌سازی تصویر نهایی
_, binary_image = cv2.threshold(mask_cleaned, 70, 255, cv2.THRESH_BINARY)

# نمایش تصویر باینری نهایی با مات‌پلات‌لیب
plt.imshow(binary_image, cmap='gray')
plt.axis('off')
plt.show()

# ذخیره تصویر نهایی
cv2.imwrite(f'output.png', binary_image)

