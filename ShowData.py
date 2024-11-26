import sqlite3

# مسیر فایل پایگاه داده SQLite
db_path = 'labeling_project/db.sqlite3'


try:
    # اتصال به پایگاه داده
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # اجرای کوئری برای دریافت اطلاعات جدول ImageData
    cursor.execute("""
        SELECT image_name, label FROM image_labeler_imagedata
        WHERE label IS NOT NULL
        AND LENGTH(label) < 2
        AND label != '-'
    """)
    
    # بازیابی تمامی سطرها
    rows = cursor.fetchall()
    
    # نمایش هر سطر
    for row in rows:
        image_name, label = row
        print(f"Image Name: {image_name}, Label: {label if label else 'No Label'}")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # اطمینان از بسته شدن اتصال
    if connection:
        connection.close()
