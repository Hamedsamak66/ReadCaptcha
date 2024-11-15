import cv2
import numpy as np
from matplotlib import pyplot as plt

# بارگذاری تصویر
image = cv2.imread('AfterCrop/1_2.png')
mask = np.zeros(image.shape[:2], np.uint8)

# مدل‌های داده برای GrabCut
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)

# کادر تقریبی اطراف پیش‌زمینه (باید بر اساس تصویر اصلی تنظیم شود)
rect = (1, 100, 100, 100)  # مقدار این متغیرها را با مکان واقعی موضوع جایگزین کنید

# اعمال الگوریتم GrabCut
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# تغییر ماسک به پس‌زمینه و پیش‌زمینه
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
image_cleaned = image * mask2[:, :, np.newaxis]

# نمایش تصویر بدون پس‌زمینه
plt.imshow(cv2.cvtColor(image_cleaned, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
