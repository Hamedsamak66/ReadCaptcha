import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_hsv_range(rgb_color, tolerance):
    color_hsv = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)[0][0]
    lower_bound = np.clip(color_hsv - tolerance, [0, 0, 0], [179, 255, 255])
    upper_bound = np.clip(color_hsv + tolerance, [0, 0, 0], [179, 255, 255])
    return lower_bound, upper_bound

def preprocess_image(image):
    # نرمال‌سازی هیستوگرام برای بهبود تصاویر
    image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image_yuv[:,:,0] = cv2.equalizeHist(image_yuv[:,:,0])
    img_output = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)
    return img_output

reference_color = [133, 233, 158]
tolerance = np.array([20, 100, 100])  # تنظیم تلورانس برای عملکرد بهتر

img = cv2.imread('AfterCrop/4_1.png')

if img is None:
    print("Error loading image.")
else:
    img = preprocess_image(img)

    lower, upper = calculate_hsv_range(reference_color, tolerance)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((3, 3), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    result = cv2.bitwise_and(img, img, mask=mask_cleaned)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    plt.imshow(result_rgb)
    plt.title('Result Image')
    plt.axis('off')
    plt.show()
