from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = Flask(__name__)

model = tf.keras.models.load_model('doodle_cnn_model.keras')

SELECTED_CLASSES = [
    "The Eiffel Tower 🗼",
    "The Mona Lisa 🖼️",
    "Airplane ✈️",
    "Angel 👼",
    "Car 🚗",
    "Cat 🐱",
    "Elephant 🐘",
    "Mountain ⛰️",
    "You ⭐",
    "Whale 🐳"
]

def prepare_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert('L').resize((28, 28))
    arr = np.array(img).astype('float32')
    if arr.mean() > 127:
        arr = 255 - arr
    arr /= 255.0
    arr = arr.reshape((1, 28, 28, 1))
    return arr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    img_bytes = img_file.read()
    x = prepare_image(img_bytes)

    predictions = model.predict(x)[0]
    predicted_index = np.argmax(predictions)
    predicted_label = SELECTED_CLASSES[predicted_index]
    confidence = float(predictions[predicted_index] * 100)

    return jsonify({
        'label': predicted_label,
        'confidence': f"{confidence:.2f}%"
    })

@app.route("/health")
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run()