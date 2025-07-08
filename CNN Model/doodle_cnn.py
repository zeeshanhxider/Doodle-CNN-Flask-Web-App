import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
from tensorflow.keras import layers, models, regularizers

# Configuration
DATA_DIR = "/QuickdrawDataset/quickdraw_npy"
SAMPLES_PER_CLASS = 115000
BATCH_SIZE = 128
EPOCHS = 3

SELECTED_CLASSES = [
    "The Eiffel Tower",
    "The Mona Lisa",
    "airplane",
    "angel",
    "car",
    "cat",
    "elephant",
    "mountain",
    "star",
    "whale"
]

NUM_CLASSES = len(SELECTED_CLASSES)

# Load Data
X, y = [], []
for label, class_name in enumerate(SELECTED_CLASSES):
    path = os.path.join(DATA_DIR, f"{class_name}.npy")
    data = np.load(path)[:SAMPLES_PER_CLASS]
    X.append(data)
    y.append(np.full(data.shape[0], label))

X = np.concatenate(X).reshape(-1, 28, 28) / 255.0
y = np.concatenate(y)

# Shuffle
indices = np.random.permutation(len(X))
X, y = X[indices], y[indices]

# Split 60% train, 20% val, 20% test
train_split = int(0.6 * len(X))
val_split = int(0.8 * len(X))

X_train, X_val, X_test = X[:train_split], X[train_split:val_split], X[val_split:]
y_train, y_val, y_test = y[:train_split], y[train_split:val_split], y[val_split:]

# Preprocessing
def preprocess(img, label, augment=False):
    img = tf.cast(img, tf.float32)
    img = tf.expand_dims(img, -1)
    if augment:
        dx = tf.random.uniform([], -3, 3, dtype=tf.int32)
        dy = tf.random.uniform([], -3, 3, dtype=tf.int32)
        img = tf.roll(img, shift=[dx, dy], axis=[0, 1])
        img = tf.image.random_flip_left_right(img)
    return img, label

train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train)).map(lambda x, y: preprocess(x, y, True)).batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)
val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val)).map(lambda x, y: preprocess(x, y)).batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)
test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test)).map(lambda x, y: preprocess(x, y)).batch(BATCH_SIZE)

# Model
l2 = regularizers.l2(1e-4)
model = models.Sequential([
    layers.Input((28, 28, 1)),

    layers.Conv2D(64, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.BatchNormalization(),
    layers.Conv2D(64, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.MaxPooling2D(2), layers.Dropout(0.25),

    layers.Conv2D(128, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.BatchNormalization(),
    layers.Conv2D(128, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.MaxPooling2D(2), layers.Dropout(0.25),

    layers.Conv2D(256, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.BatchNormalization(),
    layers.Conv2D(256, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.MaxPooling2D(2), layers.Dropout(0.25),

    layers.GlobalAveragePooling2D(),
    layers.Dense(512, activation='relu'), layers.Dropout(0.5),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
checkpoint = tf.keras.callbacks.ModelCheckpoint("quickdraw_cnn_model.keras", save_best_only=True)

history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS,
                    callbacks=[early_stop, checkpoint])

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend()
plt.title("Accuracy")

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend()
plt.title("Loss")
plt.show()

# Save model
model.save("doodle_cnn_model.keras")

# Ground truths
y_true = np.concatenate([labels.numpy() for _, labels in test_ds])

# Predictions
y_pred_probs = model.predict(test_ds)
y_pred = np.argmax(y_pred_probs, axis=1)

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=SELECTED_CLASSES, yticklabels=SELECTED_CLASSES, cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Classification report
print(classification_report(y_true, y_pred, target_names=SELECTED_CLASSES))

# Show some misclassified samples
wrong_idxs = np.where(y_true != y_pred)[0]
print(f"Total Misclassified: {len(wrong_idxs)}")

plt.figure(figsize=(12, 12))
for i, idx in enumerate(wrong_idxs[:16]):
    plt.subplot(4, 4, i+1)
    plt.imshow(X_test[idx], cmap='gray')
    plt.title(f"True: {SELECTED_CLASSES[y_true[idx]]}\nPred: {SELECTED_CLASSES[y_pred[idx]]}")
    plt.axis("off")
plt.tight_layout()
plt.show()