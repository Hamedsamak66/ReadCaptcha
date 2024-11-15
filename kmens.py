import cv2
import numpy as np
import matplotlib.pyplot as plt

# خواندن تصویر
image = cv2.imread('AfterCrop/2_2.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# بازسازی داده‌ها برای K-Means
pixels = hsv.reshape(-1, 3)
pixels = np.float32(pixels)

# مقداردهی برای K-Means
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
k = 3  # تعداد رنگ‌هایی که می‌خواهید تشخیص دهید
_, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# تبدیل به واحد 8 بیتی
centers = np.uint8(centers)

# دسته‌ای از برچسب‌ها و مراکز
dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]

# تعریف محدوده برای رنگ غالب 
lower = np.clip(dominant_color - np.array([10, 50, 50]), 0, 255)
upper = np.clip(dominant_color + np.array([10, 50, 50]), 0, 255)

# ایجاد ماسک
mask = cv2.inRange(hsv, lower, upper)

# اعمال ماسک به تصویر اصلی
result = cv2.bitwise_and(image, image, mask=mask)

result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
plt.imshow(result_rgb)
plt.axis('off')  # برای حذف نمایش محورها
plt.show()


# نمایش
#cv2.imshow('Result', result)
#cv2.waitKey(0)
#cv2.destroyAllWindows()