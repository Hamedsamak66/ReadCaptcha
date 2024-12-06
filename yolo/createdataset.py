import sqlite3
import os
import cv2

# اتصال به دیتابیس SQLite
conn = sqlite3.connect('../labeling_project/db.sqlite3')
cur = conn.cursor()

# اجرای یک کوئری برای دریافت داده‌ها
cur.execute("SELECT image_name, label FROM image_labeler_imagedata where label != '' and label != '-' AND LENGTH(label) < 2")
data = cur.fetchall()

# فرض کنید که تصاویر شما در پوشه‌ای به نام 'images/' ذخیره شده‌اند
base_image_path = '../labeling_project/image_labeler/static/images/'

# ایجاد پوشه برای برچسب‌ها
label_path_train = 'dataset/labels/train'
label_path_val = 'dataset/labels/val'

image_path_train = 'dataset/images/train'
image_path_val = 'dataset/images/val'


#os.makedirs(label_path, exist_ok=True)

# پردازش داده‌ها و ذخیره برچسب‌ها
for entry in data:
    image_name, correct_number = entry
    image_path = os.path.join(base_image_path, image_name)

    # بارگذاری تصویر و دریافت ابعاد
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    # ایجاد فایل برچسب با همان نام تصویر
    label_file = os.path.join(label_path, f"{os.path.splitext(image_name)[0]}.txt")
    with open(label_file, 'w') as f:
        # ساخت برچسب، فرض برای دوباره برچسب‌زدن باید اندازه باکس‌ها را مشخص کنید.
        # در این مثال فرض می‌کنیم که مرکز و اندازه باکس از قبل مشخص است
        center_x, center_y, box_width, box_height = (0.5, 0.5, 0.2, 0.2)  # مقادیر فرضی، باید با مقادیر واقعی جایگزین شوند.
        f.write(f"{correct_number} {center_x} {center_y} {box_width} {box_height}\n")
