import cv2
import numpy as np
import matplotlib.pyplot as plt




# خواندن تصویر
img = cv2.imread(f'AfterCrop/4_1.png')
(b, g, r) = img[0, 0]
print(f'r={r},g={g},b={b}')
rgb = np.array([133, 233, 158], dtype=np.uint8)



# مقداردهشی دقیق محدوده‌های رنگی
lower = np.array([50, 100, 100])
upper = np.array([70, 255, 255])


# تبدیل تصویر به فضای رنگی HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ایجاد ماسک برای بخش رنگ خاص
mask = cv2.inRange(hsv, lower, upper)

# استفاده از فیلتر گوسین برای نرم‌سازی
blurred = cv2.GaussianBlur(mask, (5, 5), 0)

# کاهش اندازه کرنل برای عملیات مورفولوژیکیشش
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

