
# CNN Flask Web App to Recognize Doodles

This is a full-stack web application that lets users draw doodles and classify them using a Convolutional Neural Network (CNN) trained on a subset of the [Quick, Draw! dataset](https://quickdraw.withgoogle.com/data). The backend is powered by Flask, and the model is built using TensorFlow/Keras. It supports both local and Docker-based deployment.

---

## 🚀 Features

- Draw doodles directly on a canvas and get real-time predictions
- Minimal, modern UI with light and dark modes
- Trained CNN model on 10 doodle classes from QuickDraw dataset
- Flask backend for inference and routing
- Docker support for containerized deployment

---

## 🌍 Live Demo

Try the live app here: [Doodle Detection AI Live Demo](https://zeeshanslittlecnn.onrender.com/)

---


## 🧠 CNN Architecture Details

The CNN was trained on 10 selected classes from the QuickDraw dataset and achieved a validation accuracy of 95%.

**Model Summary:**

- Input: 28x28 grayscale image (1 channel)
- Conv2D (64 filters, 3x3, ReLU, padding=same, L2 regularization)
- BatchNormalization
- Conv2D (64 filters, 3x3, ReLU, padding=same, L2 regularization)
- MaxPooling2D (2x2), Dropout (0.25)
- Conv2D (128 filters, 3x3, ReLU, padding=same, L2 regularization)
- BatchNormalization
- Conv2D (128 filters, 3x3, ReLU, padding=same, L2 regularization)
- MaxPooling2D (2x2), Dropout (0.25)
- Conv2D (256 filters, 3x3, ReLU, padding=same, L2 regularization)
- BatchNormalization
- Conv2D (256 filters, 3x3, ReLU, padding=same, L2 regularization)
- MaxPooling2D (2x2), Dropout (0.25)
- GlobalAveragePooling2D
- Dense (512, ReLU), Dropout (0.5)
- Dense (10, Softmax)

**Training Configuration:**

- Optimizer: Adam
- Loss Function: Sparse Categorical Crossentropy
- Regularization: L2 (1e-4)
- Metrics: Accuracy

---

## 🌐 Web App Structure

### 🖼 Frontend

- HTML5 Canvas for drawing doodles
- JavaScript for stroke handling and submission
- Light/Dark mode GIF preview for each class
- Responsive layout for both web and mobile

### 🧠 Backend (Flask)

- `/`: Home route rendering the canvas and UI
- `/predict`: Accepts base64 PNG from canvas, preprocesses to 28x28, runs inference with CNN model, returns prediction

---

## 📁 Folder Structure

```
Doodle-CNN-Flask-Web-App/
│
├── app.py                        # Main Flask app
│
├── CNN Model/                    
│   ├── doodle_cnn.py             # CNN Model training script
│   ├── doodle_cnn_inference.py   # Inference script for custom .png files
│   ├── doodle_cnn_model.keras    # Trained keras model
│   └── doodle_sample.png         # Custom png sample
│
├── QuickDrawDataset/                
│   └── get_dataset.py            # Run this script to download the dataset              
│   
│
├── static/                 
│   ├── styles.css                # Main stylesheet
│   ├── script.js                 # Javascript file
│   └── assets/                   # Assets 
│
├── templates/              
│   └── index.html                # Main frontend page
│
├── Dockerfile                    # Docker setup
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🛠 Installation

### 🔧 Option 1: Local Python Environment

```bash
git clone https://github.com/zeeshanhxider/Doodle-CNN-Flask-Web-App.git
cd Doodle-CNN-Flask-Web-App

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### 🐳 Option 2: Docker

```bash
docker build -t doodle-app .
docker run -p 5000:5000 doodle-app
```

Open `http://localhost:5000/` in your browser.

---

## 🔮 Future Improvements

- Add support for 100+ classes by using a LSTM + CNN hybrid
- Live prediction while drawing
- Mobile optimization
- Save and view past predictions

---

## Made with 🧡 by zeeshan