from datasets import load_dataset
import tensorflow as tf
import numpy as np
import os
import math

# ============================================================
# FOODGUARD AI - MEMORY EFFICIENT FOOD CLASSIFIER
# Hardware: 8 GB RAM
# Model: EfficientNetB0 Transfer Learning
# ============================================================

print("Loading Indian Food dataset...")

dataset = load_dataset("rajistics/indian_food_images")

# ------------------------------------------------------------
# Dataset split
# ------------------------------------------------------------

full_train = dataset["train"]
test_data = dataset["test"]

# Keep test data completely separate
split = full_train.train_test_split(
    test_size=0.20,
    seed=42,
    stratify_by_column="label"
)

train_data = split["train"]
val_data = split["test"]

class_names = full_train.features["label"].names
NUM_CLASSES = len(class_names)

print("\nDataset information")
print("-------------------")
print("Training images   :", len(train_data))
print("Validation images :", len(val_data))
print("Test images       :", len(test_data))
print("Food classes      :", NUM_CLASSES)

print("\nClasses:")
for i, name in enumerate(class_names):
    print(i, "->", name)


# ============================================================
# IMAGE SETTINGS
# ============================================================

IMG_SIZE = (224, 224)

# Small batch because your laptop has 8 GB RAM
BATCH_SIZE = 8


# ============================================================
# MEMORY-EFFICIENT DATA GENERATOR
# Images are loaded one batch at a time
# ============================================================

def image_generator(data, shuffle=False):

    indices = np.arange(len(data))

    while True:

        if shuffle:
            np.random.shuffle(indices)

        for start in range(0, len(indices), BATCH_SIZE):

            batch_indices = indices[start:start + BATCH_SIZE]

            images = []
            labels = []

            for index in batch_indices:

                item = data[int(index)]

                image = item["image"]

                # Convert to RGB
                image = image.convert("RGB")

                # Resize image
                image = image.resize(IMG_SIZE)

                # Convert to NumPy
                image = np.asarray(
                    image,
                    dtype=np.float32
                )

                images.append(image)
                labels.append(item["label"])

            yield (
                np.array(images, dtype=np.float32),
                np.array(labels, dtype=np.int32)
            )


# ============================================================
# CREATE TF DATASETS
# ============================================================

output_signature = (
    tf.TensorSpec(
        shape=(None, 224, 224, 3),
        dtype=tf.float32
    ),
    tf.TensorSpec(
        shape=(None,),
        dtype=tf.int32
    )
)

train_ds = tf.data.Dataset.from_generator(
    lambda: image_generator(train_data, shuffle=True),
    output_signature=output_signature
)

val_ds = tf.data.Dataset.from_generator(
    lambda: image_generator(val_data, shuffle=False),
    output_signature=output_signature
)

test_ds = tf.data.Dataset.from_generator(
    lambda: image_generator(test_data, shuffle=False),
    output_signature=output_signature
)

# Only keep a small amount ready in memory
train_ds = train_ds.prefetch(1)
val_ds = val_ds.prefetch(1)
test_ds = test_ds.prefetch(1)


# ============================================================
# DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.10),
    tf.keras.layers.RandomZoom(0.10)
])


# ============================================================
# EFFICIENTNETB0
# ============================================================

print("\nLoading EfficientNetB0...")

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers
base_model.trainable = False


# ============================================================
# BUILD MODEL
# ============================================================

inputs = tf.keras.Input(
    shape=(224, 224, 3)
)

x = data_augmentation(inputs)

x = base_model(
    x,
    training=False
)

x = tf.keras.layers.GlobalAveragePooling2D()(x)

x = tf.keras.layers.Dropout(0.30)(x)

outputs = tf.keras.layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = tf.keras.Model(
    inputs,
    outputs
)


# ============================================================
# COMPILE
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nModel created successfully!")

model.summary()


# ============================================================
# TRAINING SETTINGS
# ============================================================

train_steps = math.ceil(
    len(train_data) / BATCH_SIZE
)

val_steps = math.ceil(
    len(val_data) / BATCH_SIZE
)

print("\nTraining steps per epoch:", train_steps)
print("Validation steps:", val_steps)


# ============================================================
# CALLBACKS
# ============================================================

os.makedirs("models", exist_ok=True)

callbacks = [

    tf.keras.callbacks.ModelCheckpoint(
        "models/foodguard_best.keras",
        monitor="val_accuracy",
        save_best_only=True,
        mode="max"
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=3,
        restore_best_weights=True
    )
]


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n========================================")
print("STARTING FOODGUARD AI TRAINING")
print("========================================\n")

history = model.fit(
    train_ds,
    steps_per_epoch=train_steps,
    validation_data=val_ds,
    validation_steps=val_steps,
    epochs=10,
    callbacks=callbacks
)


# ============================================================
# SAVE FINAL MODEL
# ============================================================

model.save(
    "models/foodguard_food_classifier.keras"
)


# ============================================================
# SAVE CLASS NAMES
# ============================================================

with open(
    "models/class_names.txt",
    "w",
    encoding="utf-8"
) as file:

    for name in class_names:
        file.write(name + "\n")


print("\n========================================")
print("TRAINING COMPLETED!")
print("========================================")

print("\nModel saved at:")
print("models/foodguard_food_classifier.keras")

print("\nClass names saved at:")
print("models/class_names.txt")