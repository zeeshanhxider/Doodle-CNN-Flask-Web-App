import numpy as np
import tensorflow as tf
from PIL import Image

# Class names
SELECTED_CLASSES = [
    "apple",
    "butterfly",
    "camera",
    "cake",
    "clock",
    "cup",
    "dolphin",
    "elephant",
    "fish",
    "flower",
    "guitar",
    "ice cream",
    "key",
    "mountain",
    "moon",
    "octopus",
    "pizza",
    "scissors",
    "star",
    "sun",
    "train",
    "umbrella",
    "bus"
]

# Load CNN model
model = tf.keras.models.load_model('doodle_cnn_model.keras')

def load_and_prepare_image(path):
    img = Image.open(path).convert('L')         # Convert to grayscale
    img = img.resize((28, 28))                  # Resize
    img_array = np.array(img).astype('float32') # Convert to array

    # Optional: Invert if white background
    if np.mean(img_array) > 127:
        img_array = 255 - img_array
        img = Image.fromarray(img_array.astype(np.uint8))

    img_array /= 255.0                          # Normalize to 0–1
    img_array = np.expand_dims(img_array, axis=-1)  # (28,28,1)
    img_array = np.expand_dims(img_array, axis=0)   # (1,28,28,1)

    return img_array

def predict(path):
    x = load_and_prepare_image(path)
    predictions = model.predict(x)[0]
    
    predicted_index = np.argmax(predictions)
    predicted_label = SELECTED_CLASSES[predicted_index]
    confidence = predictions[predicted_index] * 100

    print(f"Predicted class: {predicted_label}")
    print(f"Confidence: {confidence:.2f}%")
    print("\nClass probabilities:")
    for i, prob in enumerate(predictions):
        print(f"{SELECTED_CLASSES[i]}: {prob * 100:.2f}%")

# Run prediction
image_path = 'doodle_sample.png'  
predict(image_path)