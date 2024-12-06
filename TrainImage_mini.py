import sqlite3
import os
import numpy as np
import cv2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

# 1. استخراج داده‌ها از پایگاه‌داده
db_path = 'labeling_project/db.sqlite3'
connection = sqlite3.connect(db_path)

query = """
 SELECT image_name, label FROM image_labeler_imagedata
        WHERE label IS NOT NULL
        AND LENGTH(label) < 2
        AND label != '-'
"""
df = pd.read_sql_query(query, connection)
connection.close()

# 2. بارگذاری تصاویر
def load_images_from_database(image_folder, df):
    images = []
    labels = []
    for _, row in df.iterrows():
        img_name = row['image_name']
        label = row['label']
        img_path = os.path.join(image_folder, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (28, 28))  # تغییر اندازه به 28x28
            images.append(img)
            labels.append(int(label))  # مطمئن شوید برچسب‌ها به صورت عددی هستند
    return np.array(images), np.array(labels)

# 3. مسیری که فایل‌های تصویری در آن قرار دارند
image_folder = 'labeling_project/image_labeler/static/images/'

# بارگذاری تصاویر و برچسب‌ها
X, y = load_images_from_database(image_folder, df)

# نرمال‌سازی داده‌ها
X = X.astype('float32') / 255
X = np.expand_dims(X, axis=-1)  # اضافه کردن بعد کانال

# تبدیل برچسب‌های عددی به دسته‌ای
y = to_categorical(y, num_classes=10)

# 4. تفکیک داده‌ها به مجموعه‌های آموزشی و آزمایشی
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. ساخت و کامپایل مدل
def create_simple_cnn(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = create_simple_cnn(X_train[0].shape)

# 6. آموزش مدل
model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)
model.save('trained_model_with_len2.h5')
# 7. ارزیابی مدل
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

print("Accuracy:", accuracy_score(y_true_classes, y_pred_classes))
print(classification_report(y_true_classes, y_pred_classes))
