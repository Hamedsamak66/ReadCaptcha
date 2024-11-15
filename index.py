import cv2
import numpy as np
import matplotlib.pyplot as plt
for i in range(1, 500):
    for j in range(1, 4):
        print(j)
        # خواندن تصویر
        img = cv2.imread(f'AfterCrop/{i}_{j}.png')
        (b, g, r) = img[0, 0]
        #r=133,b=233,g=158
        print(r, g, b)
        if 60 < g < 255 and 0 < r < 150 and 0 < b < 150:
            lower = np.array([30, 100, 100])
            upper = np.array([70, 255, 255])
        elif b > 150 and r < 100 and g < 100:
            lower = np.array([30, 90, 90])  # مقدار مثال
            upper = np.array([140, 255, 255])  # مقدار مثال
        else:
            lower = np.array([0, 0, 0])
            upper = np.array([0, 0, 0])
        '''
        if r == 160 and g == 225 and b == 95:
            # سبز
            lower = np.array([35, 100, 100])
            upper = np.array([85, 255, 255])
        elif r == 222 and g == 102 and b == 63:
            lower = np.array([5, 50, 50])
            upper = np.array([15, 255, 255])
        elif r == 220 and g == 150 and b == 80:
            lower = np.array([5, 50, 50])
            upper = np.array([15, 255, 255])
        elif r == 133 and g == 158 and b == 233:
            # مقداردهی دقیق محدوده‌های رنگی
            lower = np.array([30, 90, 90])  # مقدار مثال
            upper = np.array([140, 255, 255])  # مقدار مثال
        elif r == 223 and g == 198 and b == 123:
            # مقداردهی دقیق محدوده‌های رنگی
            lower = np.array([5, 90, 90])  # مقدار مثال
            upper = np.array([120, 255, 255])  # مقدار مثال
        elif r == 230 and g == 230 and b == 111:
            # مقداردهی دقیق محدوده‌های رنگی
            lower = np.array([30, 90, 90])  # مقدار مثال
            upper = np.array([120, 255, 255]) 
        elif r == 237 and g == 135 and b == 135:
            # مقداردهی دقیق محدوده‌های رنگی
            lower = np.array([0, 100, 100])
            upper = np.array([10, 255, 255])
        else:
            lower = np.array([5, 50, 50])
            upper = np.array([15, 255, 255])
        '''
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
        #plt.imshow(binary_image, cmap='gray')
        #plt.axis('off')
        #plt.show()

        # ذخیره تصویر نهایی
        cv2.imwrite(f'AfterPreprocessing/{i}_{j}.png', binary_image)
