import torch
import torchvision.transforms as T
from torchvision.models.segmentation import deeplabv3_resnet101
import cv2
import numpy as np
import matplotlib.pyplot as plt

# بارگذاری مدل
model = deeplabv3_resnet101(pretrained=True).eval()

# خواندن تصویر
img = cv2.imread('3.png')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# تبدیل تصویر برای ورودی مدل
trf = T.Compose([
    T.ToPILImage(),
    T.Resize(256),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_img = trf(img_rgb).unsqueeze(0)

# پیش‌بینی مدل
with torch.no_grad():
    output = model(input_img)['out'][0]
output_predictions = output.argmax(0).byte().cpu().numpy()

# بررسی کلاس‌های مختلف پیش‌بینی شده
unique_classes = np.unique(output_predictions)
print("Unique classes in the output:", unique_classes)

# انتخاب کلاس صحیح برای پیش‌زمینه
# در این مرحله باید از داده‌های زمینه‌ای برای تصمیم‌گیری درباره کلاس صحیح پیش‌زمینه استفاده شود
# ممکن است نیاز به آزمایش باشد تا کلاس صحیح را تشخیص دهید
foreground_class = unique_classes[unique_classes != 15][0]

mask = (output_predictions == foreground_class).astype(np.uint8)

# نمایش ماسک
plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(img_rgb)
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Generated Mask')
plt.imshow(mask, cmap='gray')
plt.axis('off')

# Resize ماسک
mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

# اعمال ماسک بر تصویر اصلی
img_fg = cv2.bitwise_and(img, img, mask=mask_resized)

plt.subplot(1, 3, 3)
plt.title('Masked Image')
plt.imshow(cv2.cvtColor(img_fg, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()
