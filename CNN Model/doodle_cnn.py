import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models, regularizers, initializers

# configuration
DATA_DIR = "/QuickdrawDataset/quickdraw_npy"
SAMPLES_PER_CLASS = 50000
BATCH_SIZE = 128
EPOCHS = 3

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

NUM_CLASSES = len(SELECTED_CLASSES)

X = []
y = []

# load data from .npy files
for label, class_name in enumerate(SELECTED_CLASSES):
    path = os.path.join(DATA_DIR, f"{class_name}.npy")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Make sure you've downloaded the file.")
    
    data = np.load(path)[:SAMPLES_PER_CLASS]  
    X.append(data)
    y.append(np.full(data.shape[0], label))

# stack and preprocess
X = np.concatenate(X)
X = X.reshape(-1, 28, 28)
y = np.concatenate(y)

# Normalize pixel values from 0–255 to 0–1
X = X / 255.0

# shuffle data
indices = np.random.permutation(len(X))
X = X[indices]
y = y[indices]

# split into train and test (80% train, 20% test)
split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# preprocess and augmentation
def preprocess(img, label, augment=False):
    img = tf.cast(img, tf.float32)
    img = tf.expand_dims(img, -1)  # shape: (28, 28, 1)

    if augment:
        # random horizontal shift using tf.roll
        dx = tf.random.uniform([], -3, 3, dtype=tf.int32)
        dy = tf.random.uniform([], -3, 3, dtype=tf.int32)
        img = tf.roll(img, shift=[dx, dy], axis=[0, 1])
        
        # light horizontal flip
        img = tf.image.random_flip_left_right(img)

    return img, label

# Convert labels to categorical format to use cross-entropy loss
ds_train = tf.data.Dataset.from_tensor_slices((X_train, y_train))
ds_val = tf.data.Dataset.from_tensor_slices((X_test, y_test))

# Apply preprocess
train_ds = ds_train.map(lambda x, y: preprocess(x, y, True), num_parallel_calls=tf.data.AUTOTUNE)
val_ds   = ds_val.map(lambda x, y: preprocess(x, y, False), num_parallel_calls=tf.data.AUTOTUNE)

# Batch + prefetch
train_ds = train_ds.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)
val_ds   = val_ds.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)

# model definition
l2 = regularizers.l2(1e-4)
model = models.Sequential([
    layers.Input((28, 28, 1)),
    
    layers.Conv2D(64, 3, activation='relu', padding='same', kernel_regularizer=l2, kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.Conv2D(64, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.MaxPooling2D(2), layers.Dropout(0.25),

    layers.Conv2D(128, 3, activation='relu', padding='same', kernel_regularizer=l2, kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.Conv2D(128, 3, activation='relu', padding='same', kernel_regularizer=l2),
    layers.MaxPooling2D(2), layers.Dropout(0.25),

    layers.Conv2D(256, 3, activation='relu', padding='same', kernel_regularizer=l2, kernel_initializer='he_normal'),
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

model.summary()

# callbacks for early stopping and model checkpointing
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
checkpoint = tf.keras.callbacks.ModelCheckpoint("quickdraw_cnn_model.keras", save_best_only=True, monitor='val_loss')

# train the model
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS,
                    callbacks=[early_stop, checkpoint], verbose=1)

# plot training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.legend()

plt.show()

#save the model
model.save("quickdraw_cnn_model.keras")