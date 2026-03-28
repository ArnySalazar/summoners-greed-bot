"""
Entrenamiento de clasificador CNN para Summoners Greed
Usa MobileNetV2 con transfer learning
"""
import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt

# ============ CONFIGURACION ============
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(ROOT, 'dataset', 'clasificado')
MODELS_DIR = os.path.join(ROOT, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.0001

CLASES = ['jugando', 'menu', 'monstruos', 'bonus', 'recibiste', 'continua', 'otros']

# ============ DATOS ============
print("Cargando datos...")

datagen_train = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    horizontal_flip=False,
    brightness_range=[0.8, 1.2],
    zoom_range=0.1
)

datagen_val = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = datagen_train.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    classes=CLASES
)

val_gen = datagen_val.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    classes=CLASES
)

print(f"Clases: {train_gen.class_indices}")
print(f"Train: {train_gen.samples} imagenes")
print(f"Val: {val_gen.samples} imagenes")

# ============ MODELO ============
print("\nConstruyendo modelo...")

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
output = Dense(len(CLASES), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ============ ENTRENAMIENTO ============
print("\nEntrenando...")

callbacks = [
    ModelCheckpoint(
        os.path.join(MODELS_DIR, 'mejor_modelo.keras'),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
]

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks
)

# ============ RESULTADOS ============
final_acc = max(history.history['val_accuracy'])
print(f"\n✅ Entrenamiento completo!")
print(f"Mejor accuracy: {final_acc:.2%}")
print(f"Modelo guardado en: {MODELS_DIR}/mejor_modelo.keras")

# Grafica
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title('Loss')
plt.legend()
plt.savefig(os.path.join(MODELS_DIR, 'entrenamiento.png'))
print("Grafica guardada en models/entrenamiento.png")