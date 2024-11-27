import sqlite3
import pandas as pd
import os
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. استخراج داده‌ها از پایگاه داده
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

# 2. مسیری که فایل‌های تصویری در آن قرار دارند
image_folder = '/labeling_project/image_labeler/static/images/'

# 3. پیش‌پردازش و استخراج ویژگی‌ها از تصاویر
def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features.flatten()

base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

X = []
y = df['label'].tolist()

for img_name in df['image_name']:
    img_path = os.path.join(image_folder, img_name)
    try:
        features = extract_features(img_path, model)
        X.append(features)
    except Exception as e:
        print(f"Error processing image {img_name}: {e}")

X = np.array(X)

# 4. تفکیک داده‌ها به مجموعه‌های آموزشی و آزمایشی
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. آموزش یک مدل طبقه‌بندی ساده
classifier = LogisticRegression(max_iter=1000)
classifier.fit(X_train, y_train)

# 6. ارزیابی مدل
y_pred = classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
