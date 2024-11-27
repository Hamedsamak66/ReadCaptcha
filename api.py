from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# لود کردن مدل ذخیره شده
model = tf.keras.models.load_model('trained_model.h5')

app = Flask(__name__)

def preprocess_image(image):
    img = image.resize((28, 28)).convert('L')  # تبدیل به سیاه و سفید
    img_array = np.array(img) / 255.0  # نرمال‌سازی
    img_array = np.expand_dims(img_array, axis=[0, -1])  # اضافه کردن بعد برای سازگاری با ورودی مدل
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    try:
        image = Image.open(file.stream)
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction, axis=1)[0]
        return jsonify({'predicted_class': int(predicted_class)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)