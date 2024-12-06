import cv2

# استفاده از یک مجموعه برای حذف اتوماتیک مقادیر تکراری
unique_colors = set()

for i in range(1, 500):
    img = cv2.imread(f'images/{i}.png')
    if img is not None:  # بررسی اینکه آیا تصویر به درستی خوانده شده است
        (b, g, r) = img[0, 0]
        # اضافه کردن RGB به مجموعه
        unique_colors.add((r, g, b))

# تبدیل مجموعه به یک لیست
unique_colors_list = list(unique_colors)

# ذخیره مقادیر یکتا در فایل
with open('unique_colors.txt', 'w') as file:
    for r, g, b in unique_colors_list:
        file.write(f'r={r},g={g},b={b}\n')

print("مقادیر رنگ یکتا در فایل 'unique_colors.txt' ذخیره شدند.")


    