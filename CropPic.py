from PIL import Image

# نقاط مورد نظر برای برش
cut_point1_x = 63  # نقطه اول
cut_point2_x = 117  # نقطه دوم

# اجرای عملیات برش بر روی هر تصویر
for i in range(1, 4000):
    # باز کردن تصویر
    image = Image.open(f'images/{i}.png')

    # گرفتن ابعاد تصویر
    width, height = image.size

    # برش تصویر
    slice1_box = (0, 0, cut_point1_x, height)
    slice2_box = (cut_point1_x, 0, cut_point2_x, height)
    slice3_box = (cut_point2_x, 0, width, height)

    slice1 = image.crop(slice1_box)
    slice2 = image.crop(slice2_box)
    slice3 = image.crop(slice3_box)

    # ذخیره برش‌ها به عنوان فایل‌های جدید
    slice1.save(f'AfterCrop/{i}_1.png')
    slice2.save(f'AfterCrop/{i}_2.png')
    slice3.save(f'AfterCrop/{i}_3.png')

print("تمام تصاویر با موفقیت برش داده شدند.")